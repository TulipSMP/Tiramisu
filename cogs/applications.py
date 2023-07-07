# 
# Tiramisu Discord Bot
# --------------------
# Mod Applications System
# 
from logging42 import logger
import nextcord
from nextcord.ext import commands
import yaml
from libs.database import Database
from typing import Optional

from libs import applications

class Applications(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        with open("config/config.yml", "r") as ymlfile:
            self.cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
    

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        logger.info('Loaded cog applications.py')

    # Commands
    @nextcord.slash_command(description="Create or manage Moderator Applications")
    async def application(self, interaction: nextcord.Interaction):
        pass

    @application.subcommand(description='Create an Application')
    async def create(self, interaction: nextcord.Interaction):
        await applications.ContinueConfirmation(applications.answer_and_create, text='**Start answering application questions?**', confirmed = True).start(
            interaction=interaction, ephemeral=True)
    
    @application.subcommand(description='Close this Application')
    async def close(self, interaction: nextcord.Interaction):
        await applications.close(interaction)
    

def setup(bot):
    bot.add_cog(Applications(bot))
    logger.debug('Setup cog "applications"')