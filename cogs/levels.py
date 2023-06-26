# 
# Tiramisu Discord Bot
# --------------------
# 
from logging42 import logger

import nextcord
from nextcord.ext import commands

import yaml

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
            levelling.add_points(message.author, 1)

    # Commands
    @nextcord.slash_command(description="Check your level")
    async def level(self, interaction: nextcord.Interaction):
        if type(interaction.user) != nextcord.Member:
            await interaction.send(f'Use this command in a server!')
            return
        
        msg = f'**{interaction.user.display_name}**\nLevel: {levelling.get_level(interaction.user)}\nPoints: {levelling.get_points(interaction.user)}'
        await interaction.response.send_message(msg)

def setup(bot):
    bot.add_cog(Levels(bot))
    logger.debug('Setup cog "levels"')