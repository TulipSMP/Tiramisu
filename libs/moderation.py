# 
# Tiramisu Discord Bot
# --------------------
# Moderation Actions Library
# 
from logging42 import logger
import nextcord
from nextcord.utils import escape_markdown
from typing import Optional, Union, List

import json
import uuid
import time
import os

import json
import uuid
import time

from libs.database import Database
from libs import utility, mod_database, buttons

async def modlog(guild: nextcord.Guild, subject: str, author: nextcord.User, recipient: Union[str, nextcord.User], additional: dict = {}, 
    reason: str = 'No reason specified.', moderator: bool = True, show_recipient: bool = True, action: str = None, ticket: bool = False,
    attachments: Optional[List[nextcord.Attachment]] = None, manual_log: bool = False):
    """ Send a Message in the `modlog_channel` channel
    Parameters:
     - `guild`: nextcord.Guild, which guild this message is for
     - `subject`: bold heading in messages
     - `author`: nextcord.User, who performed the action
     - `recipient`: nextcord.User or str, who the action was performed on
     - `additional`: optional dict, added fields for the message
     - `reason`: optional str, why this action was performed
     - `moderator`: optional bool, default True, set to false if the author is not a moderator.
     - `show_recipient`: optional bool, default True, whether to show the recipient ("User") field in the modlog message
     - `action`: optional str, default None, if set the action is logged in the Database and this is used in the action column
     - `ticket`: optional bool, default False, if the modlog action is a ticket. If it is, the message is sent in the `transcript_channel` channel instead, if it is set.
                    The reason is also not shown when `ticket` is enabled.
     - `attachments`: optional List[nextcord.Attachment], default None, an attachment to add
     - `manual_log`: optional bool, default False, if modlog message was manually submitted (so it can be put in `manual_modlog_channel` if set)
    Returns:
     - `str`: A message about whether this action was successful, to be put in the interaction response message """
    
    db = Database(guild, reason='Modlog, libs.moderation.modlog')
    channel = None
    
    if ticket:
        try:
            channel = guild.get_channel(int( db.fetch('transcript_channel') ))
            if channel == None:
                raise ValueError
        except ValueError:
            channel = None
    
    if manual_log:
        try:
            channel = guild.get_channel(int( db.fetch('manual_modlog_channel') ))
            if channel == None:
                raise ValueError
        except ValueError:
            channel = None
    
    if channel == None:
        try:
            channel = guild.get_channel(int( db.fetch('modlog_channel')))
            if channel == None:
                raise ValueError
        except ValueError:
            return "*Failed to log action. Make sure the `modlog_channel` setting is set to an actual channel.*"

    if moderator:
        author_title = 'Moderator'
    else:
        author_title = 'Author'
    
    if type(recipient) is str:
        recipient_display = f'\n**User:** {escape_markdown(recipient)}'
        if action != None:
            logger.warning(f'`action` was passed to modlog when `recipient` was a str! Disabling.')
            action = None
    elif show_recipient:
        recipient_display = f'\n**User:** {escape_markdown(recipient.display_name)} || {escape_markdown(recipient.name)}, `{recipient.id}` ||'
    else:
        recipient_display = ''
    message = f'## {subject}:\n**{author_title}:** {escape_markdown(author.display_name)} || {escape_markdown(author.name)}, `{author.id}` ||{recipient_display}'
    if not ticket:
        message += f'\n**Reason:** {reason}'


    for key in additional:
        message += f'\n**{key}:** {additional[key]}'

    if action != None:
        mod_database.log(db, 
            int(round(time.time() * 1000)), # timestamp
            str(uuid.uuid4()), # uuid
            action, # action codename
            str(author.id), # moderator
            str(recipient.id),
            reason,
            json.dumps(additional) # extra
            )
        db.close()

    try:
        if attachments != None:
            file_list = []
            file_paths = []
            for attachment in attachments:
                if attachment != None:
                    try:
                        cachedir = f'./.cache/'
                        try:
                            os.mkdir(cachedir)
                        except FileExistsError:
                            pass
                        filepath = f'{cachedir}/{attachment.id}-{attachment.filename}'
                        await attachment.save(filepath)

                        file = nextcord.File(filepath, attachment.filename, 
                            description=attachment.description, spoiler=attachment.is_spoiler())
                    except Exception as e:
                        response = '*Failed to log action. Could not process attachment'
                        if hasattr(e, 'message'):
                            response += f': {e}: {e.message}*'
                        else:
                            response += f': {e}*'
                        return response
                
                    file_list.append(file)
                    file_paths.append(filepath)

            await channel.send(message, files=file_list)
            
            for path in file_paths:
                os.remove(path)
        else:    
            await channel.send(message)

        return f"*Successfully logged action in {channel.mention}.*"
    except nextcord.Forbidden:
        return f"*Failed to log action. I do not have permission to send messages in {channel.mention}*"
    except BaseException as e:
        if hasattr(e, 'message'):
            extra = f'\n*{e}: {e.message}*'
        else:
            extra = f' *({e})*'
        return f'*Failed to log action. Could not send message to {channel.mention}.*{extra}'


async def kick(interaction: nextcord.Interaction, user, reason, dm=True):
    """ Kick `user` and respond to `interaction`.
        Parameters:
         - `interaction`: nextcord.Interaction for event
         - `user`: nextcord.User to kick
         - `reason`: str for why kicked """
    db = Database(interaction.guild)
    try:
        if user.bot:
            await interaction.send('I cannot kick bots!', ephemeral=True)
            return
        logger.debug(f'{interaction.user.id} kicked {user.id} for {reason}')
        try:
            if dm:
                await user.send(f"*You have been kicked from __{interaction.guild.name}__! For:*\n>>> **{reason}**")
        except nextcord.errors.HTTPException:
            await interaction.send(f'I cannot DM this user! Use the `dm` option if you do not want me to tell them why they were kicked.', ephemeral=True)
            return
        try:
            await interaction.guild.kick(user, reason=f'Kicked by {interaction.user.id} for: {reason}')
        except:
            await interaction.send(f'Could not kick {user.name}!', ephemeral=True)
            return
        logging_info = await modlog(interaction.guild, '👟 User Kicked', interaction.user, user, reason=reason, action='kick')
        await interaction.send(f'{user.mention} was successfully kicked from the server!\n{logging_info}', ephemeral=True)
    except Exception as e:
        await interaction.send(utility.error_unexpected(e, name='libs.moderation.kick'), ephemeral=True)

async def timeout(interaction: nextcord.Interaction, user: nextcord.Member, duration, reason):
    """ Timeout `user` and respond to `interaction`.
    Parameters:
     - `interaction`: nextcord.Interaction for event
     - `user`: nextcord.Member to timeout
     - `duration`: datetime.datetime or timedelta; how long to time out user
     - `reason`: str; why they were timed out """
    try:
        db = Database(interaction.guild)
        if user.bot:
            await interaction.send('I cannot timeout bots!', ephemeral=True)
            return
        logger.debug(f'{interaction.user.id} timed-out {user.id} for {reason}')
        try:
            await user.timeout(duration, reason=f'Timed out by {interaction.user.name} for: {reason}')
        except nextcord.HTTPException:
            await interaction.send(f'Could not timeout {user.name}!', ephemeral=True)
            return
        logging_info = await modlog(interaction.guild, '🛑 User Timeouted', interaction.user, user, reason=reason, additional={'Duration':f'{duration}'}, action='timeout')
        await interaction.send(f'{user.mention} was successfully timed out!\n{logging_info}', ephemeral=True)
    except Exception as e:
        await interaction.send(utility.error_unexpected(e, name='libs.moderation.timeout'), ephemeral=True)


async def ban(interaction: nextcord.Interaction, user: nextcord.Member, reason, dm=True, delete_msgs=0):
    """ Ban `user` from `interaction.guild`, and respond to `interaction`:
    Parameters:
     - `interaction`: nextcord.Interaction for this event
     - `user`: the nextcord.Member to ban
     - `reason`: why this member was banned 
     Optional:
      - `dm`: bool, whether to DM the user why they were banned (default True)
      - `delete_msgs`: int, 0 - 7, how many days of messages to delete (default 0)"""
    
    try:

        if user.bot:
            await interaction.send('I cannot ban bots!', ephemeral=True)
            return
        logger.debug(f'{interaction.user.id} banning {user.id} in {interaction.guild.id}')

        if dm:
            try:
                await user.send(f'*You have been banned from __{interaction.guild.name}__ For:*\n>>> **{reason}**')
            except nextcord.HTTPException:
                await interaction.send(f'I cannot DM this user! Use the `dm` option if you do not want me to tell them why they were kicked.', ephemeral=True)
                return
        try:
            await user.ban(reason=f'Banned by {interaction.user.name} for {reason}', delete_message_days=delete_msgs)
        except nextcord.HTTPException:
            await interaction.send('Could not ban {user.name}!', ephemeral=True)

        logging_info = await modlog(interaction.guild, '🚷 User Banned', interaction.user, user, reason=reason, additional={'DMed Reason':dm}, action='ban')
        await interaction.send(f'Banned {user.name} from this server!\n{logging_info}', ephemeral=True)

    except Exception as e:
        await interaction.send(utility.error_unexpected(e, name='libs.moderation.ban'), ephemeral=True)

async def warn(interaction: nextcord.Interaction, user: nextcord.Member, reason: str, dm: bool = True, broadcast: bool = True):
    """ Warn `user` via DM and/or public message
    Parameters:
     - `interaction`: nextcord.Interaction for this event
     - `user`: the nextcord.Member to warn
     - `reason`: warn message
     Optional:
      - `dm`: bool, whether to DM the warn to the user (default True)
      - `broadcast`: bool, whether to publicly send the warn in the current channel (default True) """
    try:
        if user.bot:
            await interaction.send('I cannot warn bots!', ephemeral=True)
            return
        logger.debug(f'{interaction.user.id} warned {user.id} for {reason}')

        if not dm and not broadcast:
            await interaction.send('How am I supposed to warn them? Enable `dm` or `broadcast`.')
            return

        if dm:
            try:
                await user.send(f"*You have been warned in __{interaction.guild.name}__! For:*\n>>> **{reason}**")
            except nextcord.HTTPException:
                await interaction.send(f'I cannot DM this user! Use the `dm` option to disable', ephemeral=True)
                return
        if broadcast:
            await interaction.channel.send(f"{user.mention} has been warned for:\n>>> **{reason}**")
        
        logging_info = await modlog(interaction.guild, '⚠️ User Warned', interaction.user, user, reason=reason, additional={'DMed':dm, 'Publicly Broadcast':broadcast}, action='warn')
        await interaction.send(f'{user.mention} was successfully warned!\n{logging_info}', ephemeral=True)

    except Exception as e:
        await interaction.send(utility.error_unexpected(e), ephemeral=True)