# 
# Tiramisu Discord Bot
# --------------------
# Logging for Moderators
# 
import nextcord
from libs.database import Database

class LoggingEvent:
    def __init__(self, guild: nextcord.Guild, title: str, user: nextcord.User, extra: dict = {}):
        """ Base class for logging events
        Parameters:
         - `guild`: nextcord.Guild, the guild this is happening in
         - `title`: str, the heading for the log message
         - `user`: nextcord.User, the doer of the action
         - `extra`: optional dict, fields for the message """

        self.guild = guild
        self.title = title
        self.user = user
        self.extra = extra
        self.void = False # Used to check if an action should be logged
    
    def message(self):
        msg = f"{self.title}\nAuthor: {self.user.name} `{self.user.id}`"
        for key in self.extra:
            msg += f"\n{key}: {self.extra[key]}"
        return msg

class DeletedMessage(LoggingEvent):
    def __init__(self, message: nextcord.Message):
        """ Event for a message being deleted """
        attachments = ''
        for attachment in message.attachments:
            if attachments == '':
                attachments += attachment.filename
            else:
                attachments += f', {attachment.filename}'
        if attachments == '':
            attachments = 'None'

        super().__init__(
            message.guild, 
            "**🗑️ Deleted Message **", 
            message.author,
            extra = {
                "Channel":message.channel.mention,
                "Content":nextcord.utils.escape_markdown(message.clean_content).replace('\n', '⮒'),
                "Attachments":attachments
            }
            )

class EditedMessage(LoggingEvent):
    def __init__(self, old: nextcord.Message, new:nextcord.Message):
        """ Event for message being edited """
        super().__init__(
            old.guild,
            "**✏️ Edited Message **",
            old.author,
            extra = {
                "Channel":old.channel.mention,
                "Old Content":nextcord.utils.escape_markdown(old.clean_content).replace('\n', '⮒'),
                "Old Attachments":self._get_attachments(old),
                "New Content":nextcord.utils.escape_markdown(new.clean_content).replace('\n', '⮒'),
                "New Attachments":self._get_attachments(new)
            }
        )

        if old.content == new.content and old.attachments == new.attachments:
            self.void = True # Only send message if content changed
        elif old.author.bot:
            self.void = True # Don't handle bot message edits (otherwise a log message is sent every interaction
                             #                  because interaction messages are sent empty and then edited)
    
    def _get_attachments(self, message: nextcord.Message):
        attachments = ''
        for attachment in message.attachments:
            if attachments == '':
                attachments += attachment.filename
            else:
                attachments += f', {attachment.filename}'
        if attachments == '':
            attachments = 'None'
        
        return attachments

class ChangeVoice(LoggingEvent):
    def __init__(self, member: nextcord.Member, before: nextcord.VoiceState, after: nextcord.VoiceState):
        """ Event for Voice state update """
        if before.channel == None and after.channel != None: # User joined a VC
            action = 'Joined'
            use = after
        elif before.channel != None and after.channel == None: # User left VC
            action = 'Left'
            use = before
        elif before.channel != None and after.channel != None and before.channel != after.channel: # User changed VCs
            super().__init__(
                member.guild, f"**🎤 Changed VC**",
                member, extra = {
                    "Previous VC":before.channel.mention,
                    "Current VC":after.channel.mention
                }
            )
            return
        elif before.self_stream and not after.self_stream:
            action = '__Stopped__ Streaming in'
            use = after
        elif not before.self_stream and after.self_stream:
            action = '__Started__ Streaming in'
            use = after
        elif before.self_video and not after.self_video:
            action = 'Turned __OFF__ Camera in'
            use = after
        elif not before.self_video and after.self_video:
            action = 'Turned __ON__ Camera in'
            use = after
        else:
            action = 'Null'
            self.void = True # Its some other change we don't want to report
        
        if not self.void:
            super().__init__(
                    member.guild, f"**🎤 {action} VC**",
                    member, extra = {
                        "VC":use.channel.mention
                    }
                )



async def log(event: LoggingEvent):
    """ Send a log message in `log_channel` returned from event.message() """
    if not event.void:
        db = Database(event.guild, reason='Logging, fetch `log_channel`')
        try:
            channel = event.guild.get_channel(int(db.fetch('log_channel')))
            if channel == None:
                raise ValueError
        except ValueError:
            return

        await channel.send(event.message())