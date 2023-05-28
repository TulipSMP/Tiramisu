# 
# Tiramisu Discord Bot
# --------------------
# Moderation Actions Library
# 
from logging42 import logger
import nextcord

from libs.database import Database
from libs import utility

async def modlog(guild: nextcord.Guild, subject: str, author: nextcord.User, recipient: nextcord.User, additional=None, reason='No reason specified.'):
    """ Send a Message in the `modlog_channel` channel
    Parameters:
     - `guild`: nextcord.Guild, which guild this message is for
     - `subject`: bold heading in messages
     - `author`: nextcord.User, who performed the action
     - `recipient`: nextcord.User, who the action was performed on
     - `additional`: optional dict, added fields for the message
     - `reason`: optional str, why this action was performed
    Returns:
     - `str`: A message about whether this action was successful, to be put in the interaction response message """
    
    db = Database(guild, reason='Fetching `modlog_channel` in libs.moderation.modlog')
    
    try:
        channel = nextcord.get_channel(int( db.fetch('modlog_channel')))
        if channel == None:
            raise ValueError
    except ValueError:
        return "*Failed to log action. Make sure the `modlog_channel` setting is set to an actual channel.*"

    message = f'**{subject}:**\nModerator: {author.display_name} ||{author.name}, `{author.id}`||\nUser: {recipient.display_name} ||{recipient.name}, `{recipient.id}`'
    
    if additional != None and type(additional) == type(dict()):
        for key in additional:
            message += f'{key}: {additional[key]}'
    
    try:
        await channel.send(message)
        return f"*Successfully logged action in {channel.mention}.*"
    except nextcord.HTTPException:
        return f"*Failed to log action. I do not have permission to send messages in {channel.mention}*"
    except:
        return f'*Failed to log action. Could not send message to {channel.mention}.*'


async def kick(interaction: nextcord.Interaction, bot, user, reason, dm=True):
    """ Kick `user` and respond to `interaction`.
        Parameters:
         - `interaction`: nextcord.Interaction for event
         - `bot`: the nextcord.User object for this bot
         - `user`: nextcord.User to kick
         - `reason`: str for why kicked """
    db = Database(interaction.guild)
    try:
        if user.id == bot.id:
            await interaction.send('I cannot kick myself! If you want me to leave, have an admin kick me.')
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
        try:
            modlog_channel = interaction.guild.get_channel( int(db.fetch('modlog_channel')) )
            if modlog_channel != None:
                await modlog_channel.send(f'{user.mention} ||{user.name}#{user.discriminator} ID: `{user.id}`|| was kicked by {interaction.user.name}#{interaction.user.discriminator} ID: `{interaction.user.id}`\nFor: {reason}')
                logging_info = f'This action was logged successfully in {modlog_channel.mention}.'
            else:
                logging_info = f'This action was not logged. Make sure the `modlog_channel` setting is correct.'
        except:
            logging_info = f'This action was not logged. Make sure the `modlog_channel` setting is correct.'
        await interaction.send(f'{user.mention} was successfully kicked from the server!\n*{logging_info}*', ephemeral=True)
    except Exception as e:
        await interaction.send(utility.error_unexpected(e, name='libs.moderation.kick'), ephemeral=True)

async def timeout(interaction: nextcord.Interaction, bot: nextcord.User, user: nextcord.Member, duration, reason):
    """ Timeout `user` and respond to `interaction`.
    Parameters:
     - `interaction`: nextcord.Interaction for event
     - `bot`: the nextcord.User object for this bot
     - `user`: nextcord.Member to timeout
     - `duration`: datetime.datetime or timedelta; how long to time out user
     - `reason`: str; why they were timed out """
    try:
        db = Database(interaction.guild)
        if user.id == bot.id:
            await interaction.send('I cannot timeout myself!')
            return
        logger.debug(f'{interaction.user.id} timed-out {user.id} for {reason}')
        try:
            await user.timeout(duration, reason=f'Kicked by {interaction.user.name} for: {reason}')
        except nextcord.HTTPException:
            await interaction.send(f'Could not timeout {user.name}!', ephemeral=True)
            return
        try:
            modlog_channel = interaction.guild.get_channel( int(db.fetch('modlog_channel')) )
            if modlog_channel != None:
                await modlog_channel.send(f'{user.mention} ||{user.name} ID: `{user.id}`|| was timed-out by {interaction.user.name} ID: `{interaction.user.id}`\n\
                    For: {reason}')
                logging_info = f'This action was logged successfully in {modlog_channel.mention}.'
            else:
                logging_info = f'This action was not logged. Make sure the `modlog_channel` setting is correct.'
        except:
            logging_info = f'This action was not logged. Make sure the `modlog_channel` setting is correct.'
        await interaction.send(f'{user.mention} was successfully timed out!\n*{logging_info}*', ephemeral=True)
    except Exception as e:
        await interaction.send(utility.error_unexpected(e, name='libs.moderation.timeout'), ephemeral=True)