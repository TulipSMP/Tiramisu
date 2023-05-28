from logging42 import logger
import nextcord
from nextcord.ext import commands
import yaml
import datetime

from libs.database import Database
from libs import utility, moderation

from typing import Optional

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        with open("config/config.yml", "r") as ymlfile:
            self.cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)


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
        if interaction.user.id in db.fetch('admins') or utility.is_mod(interaction.user, db):
            try:
                if user.id == self.bot.user.id:
                    await interaction.send('I cannot warn myself!')
                    return
                logger.debug(f'{interaction.user.id} warned {user.id} for {reason}')
                try:
                    await user.send(f"*You have been warned in __{interaction.guild.name}__! For:*\n>>> **{reason}**")
                except nextcord.errors.HTTPException:
                    await interaction.send(f'I cannot DM this user!', ephemeral=True)
                    return
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
            await interaction.send(self.cfg['messages']['noperm'], ephemeral=True)
    
    @nextcord.slash_command(description="Kick a user from the server")
    async def kick(self, interaction: nextcord.Interaction, user: Optional[nextcord.Member] = nextcord.SlashOption(description='Who to kick', required=True), 
        reason: Optional[str] = nextcord.SlashOption(description='Why this user is being kicked.', default='No reason given.', required=False),
        dm: Optional[bool] = nextcord.SlashOption(description='Should the user be DMed about why they were kicked?', choices={'Yes':True, 'No':False}, required=False, default=True)):
        """ Kick a User from the guild """

        db = Database(interaction.guild, reason=f'Check for permission, `/kick`')
        if interaction.user.id in db.fetch('admins') or utility.is_mod(interaction.user, db):
            await moderation.kick(interaction, self.bot.user, user, reason, dm=dm)
        else:
            await interaction.send(self.cfg['messages']['noperm'], ephemeral=True)

    @nextcord.slash_command(description="Time out a user")
    async def timeout(self, interaction: nextcord.Interaction, user: Optional[nextcord.Member] = nextcord.SlashOption(description='Who to time out', required=True), 
        duration: Optional[str] = nextcord.SlashOption(description='How long to time out the user',
            choices={'Remove Timeout': 'rm', '30 seconds':'30s', '2 minutes':'2min', '5 minutes':'5min', '10 minutes':'20min', '30 minutes':'30min', '1 hour':'1hr',
                '6 hours':'6hr', '1 day':'1d', '3 days':'3d', '5 days':'5d', '1 week':'1w'},
                    required=True),
        reason: Optional[str] = nextcord.SlashOption(description='Why this user is being timed out.', default='No reason given.', required=False)):
        """ Timeout a Member in the guild """
        
        # Nextcord Typehints do not allow timedeltas
        # Instead, we must use string keys and translate.
        # Discord cannot handle timeouts of more than 1 week.
        delta_translation = {
            'rm' : None,
            '30s' : datetime.timedelta(seconds=30.0),
            '2min' : datetime.timedelta(minutes=2.0),
            '5min' : datetime.timedelta(minutes=5.0),
            '10min' : datetime.timedelta(minutes=10.0),
            '30min' : datetime.timedelta(minutes=30.0),
            '1hr' : datetime.timedelta(hours=1.0),
            '6hr' : datetime.timedelta(hours=6.0),
            '1d' : datetime.timedelta(days=1.0),
            '3d' : datetime.timedelta(days=3.0),
            '5d' : datetime.timedelta(days=5.0),
            '1w' : datetime.timedelta(weeks=1.0),
        }
        duration_delta = delta_translation[duration]

        db = Database(interaction.guild, reason=f'Check for permission, `/kick`')
        if interaction.user.id in db.fetch('admins') or utility.is_mod(interaction.user, db):
            await moderation.timeout(interaction, self.bot.user, user, duration_delta, reason)
        else:
            await interaction.send(self.cfg['messages']['noperm'], ephemeral=True)

def setup(bot):
    bot.add_cog(Moderation(bot))
    logger.debug('Setup cog "moderation"')