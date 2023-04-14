from logging42 import logger
import nextcord
from nextcord.ext import commands
import yaml
from libs.database import Database
from typing import Optional

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        with open("config/config.yml", "r") as ymlfile:
            self.cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
    
    # Error Function
    def error(self, error):
        logger.error(f"Error in moderation.py: {error}")
        return self.cfg['messages']['error'].replace('[[error]]', str(error))

    # No Permission Function
    def noperm(self, cmd, interaction):
        #logger.debug(self.cfg['messages']['noperm_log'].replace('[[user]]', interaction.user.name).replace('[[user_id]]', interaction.user.id).replace('[[command]]', cmd))
        return self.cfg['messages']['noperm']

    # Check if they're a mod
    def is_mod(self, user, db):
        role = user.get_role(int(db.fetch('staff_role')))
        if role == None:
            return False
        else:
            return True

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        logger.info('Loaded cog moderation.py!')

    # Commands
    @nextcord.slash_command(description="Warn a User")
    async def warn(self, interaction: nextcord.Interaction, user: Optional[nextcord.Member] = nextcord.SlashOption(description='Who to kick', required=True), 
        reason: Optional[str] = nextcord.SlashOption(description='Why this user is being warned.', default='No reason given.', required=False),
        show_message: Optional[bool] = nextcord.SlashOption(description='If a warn message should be sent in your current channel, in addition to the warn.', default=True)):
        """ Warn a User """
        db = Database(interaction.guild, reason=f'Check for permission, `/warn`')
        if interaction.user.id in db.fetch('admins') or self.is_mod(interaction.user, db):
            try:
                if user.id == self.bot.user.id:
                    await interaction.send('I cannot warn myself!')
                    return
                logger.debug(f'{interaction.user.id} warned {user.id} for {reason}')
                try:
                    await user.send(f"*You have been warned in __{interaction.guild.name}__! For:*\n>>> **{reason}**")
                except nextcord.errors.HTTPException:
                    await interaction.send(f'I cannot DM this user!', ephemeral=True)
                if show_message:
                    await interaction.channel.send(f"{user.mention} has been warned for:\n{reason}")
                try:
                    modlog_channel = interaction.guild.get_channel( int(db.fetch('modlog_channel')) )
                    if modlog_channel != None:
                        await modlog_channel.send(f'{user.mention} was warned by {interaction.user.name}#{interaction.user.discriminator} ID: `{interaction.user.id}`\nFor: {reason}')
                        logging_info = f'This action was logged successfully in {modlog_channel.mention}.'
                    else:
                        logging_info = f'This action was not logged. Make sure the `modlog_channel` setting is correct.'
                except:
                    logging_info = f'This action was not logged. Make sure the `modlog_channel` setting is correct. And {self.bot.name} has access to it.'
                await interaction.send(f'{user.mention} was successfully warned!\n*{logging_info}*', ephemeral=True)
            except Exception as e:
                await interaction.send(self.error(e), ephemeral=True)
        else:
            await interaction.send(self.noperm('warn', interaction), ephemeral=True)
    
    @nextcord.slash_command(description="Kick a user from the server")
    async def kick(self, interaction: nextcord.Interaction, user: Optional[nextcord.Member] = nextcord.SlashOption(description='Who to kick', required=True), 
        reason: Optional[str] = nextcord.SlashOption(description='Why this user is being kicked.', default='No reason given.', required=False),
        dm: Optional[bool] = nextcord.SlashOption(description='Should the user be DMed about why they were kicked?', choices={'Yes':True, 'No':False}, required=False, default=True)):
        """ Kick a User from the server """
        db = Database(interaction.guild, reason=f'Check for permission, `/kick`')
        if interaction.user.id in db.fetch('admins') or self.is_mod(interaction.user, db):
            try:
                if user.id == self.bot.user.id:
                    await interaction.send('I cannot kick myself! If you want me to leave, have an admin kick me.')
                    return
                logger.debug(f'{interaction.user.id} kicked {user.id} for {reason}')
                try:
                    await user.send(f"*You have been kicked from __{interaction.guild.name}__! For:*\n>>> **{reason}**")
                except nextcord.errors.HTTPException:
                    await interaction.send(f'I cannot DM this user! Use the `dm` option if you do not want me to tell them why they were kicked.')
                try:
                    modlog_channel = self.client.get_channel( int(db.fetch('modlog_channel')) )
                    if modlog_channel != None:
                        await modlog_channel.send(f'{user.mention} ||{user.name}#{user.discriminator} ID: `{user.id}`|| was kicked by {interaction.user.name}#{interaction.user.discriminator} ID: `{interaction.user.id}`\nFor: {reason}')
                        logging_info = f'This action was logged successfully in {modlog_channel.mention}.'
                    else:
                        logging_info = f'This action was not logged. Make sure the `modlog_channel` setting is correct.'
                except:
                    logging_info = f'This action was not logged. Make sure the `modlog_channel` setting is correct.'
                await interaction.send(f'{user.mention} was successfully kicked from the server!\n*{logging_info}*', ephemeral=True)
            except Exception as e:
                await interaction.send(self.error(e), ephemeral=True)
        else:
            await interaction.send(self.noperm('kick', interaction), ephemeral=True)

def setup(bot):
    bot.add_cog(Moderation(bot))
    logger.debug('Setup cog "moderation"')