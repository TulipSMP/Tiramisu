# 
# Tiramisu Discord Bot
# --------------------
# Moderation Commands
# 
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
    async def warn(self, interaction: nextcord.Interaction, user: Optional[nextcord.Member] = nextcord.SlashOption(description='Who to warn', required=True), 
        reason: Optional[str] = nextcord.SlashOption(description='Why this user is being warned.', required=True),
        broadcast: Optional[bool] = nextcord.SlashOption(description='If a warn message should be sent in your current channel.', default=True),
        dm: Optional[bool] = nextcord.SlashOption(description='Whether to DM a warn message to the user.', default=True)):
        """ Warn a User """
        db = Database(interaction.guild, reason=f'Check for permission, `/warn`')
        if interaction.user.id in db.fetch('admins') or utility.is_mod(interaction.user, db):
            await moderation.warn(interaction, user, reason, dm=dm, broadcast=broadcast)
        else:
            await interaction.send(self.cfg['messages']['noperm'], ephemeral=True)
    
    @nextcord.slash_command(description="Kick a user from the server")
    async def kick(self, interaction: nextcord.Interaction, user: Optional[nextcord.Member] = nextcord.SlashOption(description='Who to kick', required=True), 
        reason: Optional[str] = nextcord.SlashOption(description='Why this user is being kicked.', default='No reason given.', required=False),
        dm: Optional[bool] = nextcord.SlashOption(description='Should the user be DMed about why they were kicked?', choices={'Yes':True, 'No':False}, required=False, default=True)):
        """ Kick a User from the guild """

        db = Database(interaction.guild, reason=f'Check for permission, `/kick`')
        if interaction.user.id in db.fetch('admins') or utility.is_mod(interaction.user, db):
            await moderation.kick(interaction, user, reason, dm=dm)
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
            await moderation.timeout(interaction, user, duration_delta, reason)
        else:
            await interaction.send(self.cfg['messages']['noperm'], ephemeral=True)

    @nextcord.slash_command(description="Ban a user from your server")
    async def ban(self, interaction: nextcord.Interaction, user: Optional[nextcord.Member] = nextcord.SlashOption(description='Who to ban', required=True),
        reason: Optional[str] = nextcord.SlashOption(description='Why this user is being banned.', required=True),
        delete_message_days: Optional[int] = nextcord.SlashOption(description='How many days of their message history to delete', required=False, default=0,
            choices={'0 days':0, '1 day':1, '2 days':2, '3 days':3, '4 days':4, '5 days':5, '6 days':6, '7 days':7}),
        dm: Optional[bool] = nextcord.SlashOption(description='Whether to DM the user about why they were banned', required=False, default=True)):
        """ Ban a User from the Guild """
        db = Database(interaction.guild, reason='Check for permission, `/ban`')
        if interaction.user.id in db.fetch('admins') or utility.is_mod(interaction.user, db):
            
            await  moderation.ban(interaction, user, reason, dm=dm, delete_msgs=delete_message_days)

        else:
            await interaction.send(self.cfg['messages']['noperm'])
    
    @nextcord.slash_command()
    async def log(self, interaction: nextcord.Interaction):
        pass
        # Setup for subcommands
    
    @log.subcommand(description='Log a punishment from outside of discord')
    async def punishment(self, interaction: nextcord.Interaction, 
        action: Optional[str] = nextcord.SlashOption(required=True, description='Type of punishment dealt',
            choices = ['Warned', 'Muted', 'Kicked', 'Tempbanned', 'Banned', 'IP Muted', 'IP Tempbanned', 'IP Banned']),
        username: Optional[str] = nextcord.SlashOption(required=True, description='The user who was punished'),
        uuid: Optional[str] = nextcord.SlashOption(required=True, description='ID or UUID of the punished player'),
        platform: Optional[str] = nextcord.SlashOption(required=True, description='Platform the user is on'),
        reason: Optional[str] = nextcord.SlashOption(required=True, description='Reasoning for dealing punishment'),
        duration: Optional[str] = nextcord.SlashOption(required=False, description='Duration of punishment (if temporary)'),
        notes: Optional[str] = nextcord.SlashOption(required=False, description='Extra Information about the event'),
        ticket: Optional[nextcord.TextChannel] = nextcord.SlashOption(required=False, description='Ticket channel with this incident'),
        attachments: Optonal[nextcord.Attachment] = nextcord.SlashOption(required=False, description='Screenshots of evidence or other related information.')):
        
        db = Database(interaction.guild, reason='Moderation, log punishment')
        if interaction.user in db.fetch('admins') or utility.is_mod(interaction.user, db):
            if duration == None:
                duration = 'Permanent'
            additional = {
                    'UUID': uuid,
                    'Platform': platform,
                    'Notes': notes,
                    'Ticket': ticket.mention,
                }

            await moderation.modlog(
                interaction.guild,
                subject = f'🛠️ Externally {action} User',
                author = interaction.user,
                recipient = username,
                reason = reason,
                additional = additional,
                # TODO: Attachments support
                #attachments = attachments
            )
        else:
            await interaction.send(self.cfg['messages']['noperm'])

def setup(bot):
    bot.add_cog(Moderation(bot))
    logger.debug('Setup cog "moderation"')