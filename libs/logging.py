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
    
    def message(self):
        msg = f"{self.title}\nBy: {self.user.name} `{self.user.id}`"
        for key in self.extra:
            msg += f"\n{key}: __{self.extra[key]}__"
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
            "**✏️ Deleted Message **", 
            message.author,
            extra = {
                "Channel":message.channel.mention,
                "Content":message.content,
                "Attatchments":attachments
            }
            )


async def log(event: LoggingEvent):
    db = Database(event.guild, reason='Logging, fetch `log_channel`')
    try:
        channel = event.guild.get_channel(int(db.fetch('log_channel')))
        if channel == None:
            raise ValueError
    except ValueError:
        return
    
    await channel.send(event.message())