# 
# Tiramisu Discord Bot
# --------------------
# Right-Click Mod Actions
# 
from logging42 import logger

import yaml
import nextcord
from nextcord.ext import commands

from libs.database import Database
from libs import moderation, utility

class ModRightclick(commands.Cog):
    def __init__(self, bot):
        """ Perform moderation actions by right-clicking users """
        self.bot = bot    
        with open("config/config.yml", "r") as ymlfile:
            self.cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)


    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        logger.info('Loaded cog mod_rightclick.py')

    # Commands
    @nextcord.user_command()
    async def test(interaction: nextcord.Interaction, member: nextcord.Member):
        await interaction.send(f'Hiya {member.mention}')

def setup(bot):
    bot.add_cog(ModRightclick(bot))
    logger.debug('Setup cog "mod_rightclick"')