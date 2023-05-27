# 
# Tiramisu Discord Bot
# --------------------
# Moderation Actions Library
# 
from logging42 import logger
import nextcord

from libs.database import Database
from libs import utility


def kick(interaction: nextcord.Interaction, user, dm=True):
    """ Kick `user` and respond to `interaction`.
        Parameters:
         - `interaction`: nextcord.Interaction for event
         - `user`: nextcord.User to kick
         - `reason`: str for why kicked """
    db = Database(interaction.guild)
    try:
        if user.id == self.bot.user.id:
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
            interaction.guild.kick(user)
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
        utility.error_unexpected(interaction, e)