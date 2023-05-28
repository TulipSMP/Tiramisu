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
        channel = guild.get_channel(int( db.fetch('modlog_channel')))
        if channel == None:
            raise ValueError
    except ValueError:
        return "*Failed to log action. Make sure the `modlog_channel` setting is set to an actual channel.*"

    message = f'**{subject}:**\nModerator: __{author.display_name}__ || {author.name}, `{author.id}` ||\nUser: __{recipient.display_name}__ || {recipient.name}, `{recipient.id}` ||\nReason: __{reason}__'

    if additional != None and type(additional) == type(dict()):
        for key in additional:
            message += f'\n{key}: __{additional[key]}__'
    
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
        logging_info = await modlog(interaction.guild, 'User Kicked', interaction.user, user, reason=reason)
        await interaction.send(f'{user.mention} was successfully kicked from the server!\n{logging_info}', ephemeral=True)
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
            await user.timeout(duration, reason=f'Timed out by {interaction.user.name} for: {reason}')
        except nextcord.HTTPException:
            await interaction.send(f'Could not timeout {user.name}!', ephemeral=True)
            return
        logging_info = await modlog(interaction.guild, 'User Timeouted', interaction.user, user, reason=reason, additional={'Duration':f'{duration}'})
        await interaction.send(f'{user.mention} was successfully timed out!\n{logging_info}', ephemeral=True)
    except Exception as e:
        await interaction.send(utility.error_unexpected(e, name='libs.moderation.timeout'), ephemeral=True)

async def ban(interaction: nextcord.Interaction, bot: nextcord.User, user: nextcord.Member, reason, dm=True):
    """ Ban `user` from `interaction.guild`, and respond to `interaction`:
    Parameters:
     - `interaction`: nextcord.Interaction for this event
     - `bot`: the nextcord.User for this bot
     - `user`: the nextcord.Member to ban
     - `reason`: why this member was banned """
    
    try:
        if user.id == bot.id:
            await interaction.send('I cannot ban myself!')
            return
        logger.debug(f'{interaction.user.id} banning {user.id} in {interaction.guild.id}')

        if dm:
            try:
                await user.send(f'*You have been banned from __{interaction.guild.name}__ For:*\n>>>{reason}')
            except nextcord.HTTPException:
                await interaction.send(f'I cannot DM this user! Use the `dm` option if you do not want me to tell them why they were kicked.', ephemeral=True)
                return
        try:
            await user.ban(reason=f'Banned by {interaction.user.name} for {reason}')
        except nextcord.HTTPException:
            await interaction.send('Could not ban {user.name}!', ephemeral=True)

        logging_info = modlog(interaction.guild, 'User Banned', interaction.user, user, reason=reason, additional={'DMed Reason':dm})
        await interaction.send()

    except Exception as e:
        await interaction.send(utility.error_unexpected(e, name='libs.moderation.ban'), ephemeral=True)

    pass