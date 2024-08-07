# 
# Tiramisu Discord Bot
# --------------------
# 
from logging42 import logger

import nextcord
from nextcord.ext import commands

import yaml
import random
import asyncio
from typing import Optional

from libs.database import Database
from libs import utility, moderation, levelling

class Levels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
        with open("config/config.yml", "r") as ymlfile:
            self.cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        logger.info('Loaded cog levels.py')
    
    @commands.Cog.listener()
    async def on_message(self, message: nextcord.message):
        if message.author.bot:
            return
        elif type(message.author) == nextcord.Member:
            db = Database(message.guild, reason='Levels, check `no_points_channels`')
            no_points = db.fetch('no_points_channels')
            if 'all' in no_points.strip():
                return
            elif str(message.channel.id) in no_points:
                return

            prev_level = levelling.get_level(message.author)

            levelling.add_points(message.author, random.randint(1, 3))
            
            new_level = levelling.get_level(message.author)
            if new_level > prev_level:
                if not message.channel.type == nextcord.ChannelType.news:
                    message = await message.channel.send(f'**⬆️ {message.author.mention} is now at level {new_level}!**')
                else:
                    message = await message.author.send(f'**⬆️ You have reached level {new_level} in {message.guild.name}!**')
                
                await message.delete(delay = 120)

    # Commands
    @nextcord.slash_command(description="Check your level")
    async def level(self, interaction: nextcord.Interaction):
        if type(interaction.user) != nextcord.Member:
            await interaction.send(f'Use this command in a server!')
            return
        db = Database(interaction.guild, reason='Levels, settings check')
        if 'all' in db.fetch('no_points_channels'):
            await interaction.send(self.cfg['messages']['noperm'], ephemeral=True)
        else:
            msg = f'**{interaction.user.display_name}**\nLevel: {levelling.get_level(interaction.user)}\nPoints: {levelling.get_points(interaction.user)}'
            await interaction.response.send_message(msg)
    
    @nextcord.slash_command(description="Points Leaderboard")
    async def leveltop(self, interaction: nextcord.Interaction):
        db = Database(interaction.guild, reason='Levels, settings check')
        if 'all' in db.fetch('no_points_channels'):
            await interaction.send(self.cfg['messages']['noperm'], ephemeral=True)
        else:
            leaders = levelling.get_leaderboard(interaction.guild)

            msg = '**Leaderboard:**'
            for user_id in leaders:
                try:
                    user = self.bot.get_user(int(user_id))
                    if user == None:
                        raise ValueError
                except ValueError:
                    continue
                msg += f'\n{user.display_name} - {leaders[user_id]} pts *Level {levelling.get_level(user, cached_pts=leaders[user_id])}*'
            
            await interaction.send(msg)

    @nextcord.slash_command(description='Reset a user\'s points')
    async def resetlevel(self, interaction: nextcord.Interaction, 
        member: Optional[nextcord.Member] = nextcord.SlashOption(description='User to reset points for', required=True),
        reason: Optional[str] = nextcord.SlashOption(description='Why you are resetting points', required=False)):
        db = Database(interaction.guild, reason='Level reset, check perms')
        if utility.is_mod(interaction.user, db) or interaction.user.id in db.fetch('admins'):
            levelling.reset_points(member)
            await moderation.modlog(interaction.guild, f'💯 Reset Points', interaction.user, member, reason=reason)
            await interaction.send(f'Reset points for {member.display_name}.', ephemeral=True)
        else:
            await interaction.send(self.cfg['messages']['noperm'])

def setup(bot):
    bot.add_cog(Levels(bot))
    logger.debug('Setup cog "levels"')