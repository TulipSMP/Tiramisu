# 
# Tiramisu Discord Bot
# --------------------
# Moderation Actions Library
# 
from logging42 import logger
import nextcord

from libs.database import Database
from libs import utility


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