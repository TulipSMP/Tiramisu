from logging42 import logger
import nextcord
from nextcord.ext import commands
import yaml
from libs.database import Database

class Catboy(commands.Cog):
    def __init__(self, bot):
        """ Boilerplate Cog. Also funny fizzdev catboy hahaha """
        self.bot = bot    
        with open("config/config.yml", "r") as ymlfile:
            self.cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)


    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        logger.info('Loaded cog catboy.py')

    # Commands
    @nextcord.slash_command(description="Try me!")
    async def fizz(self, interaction: nextcord.Interaction):
        await interaction.send(f"Yes, fizz is indeed a catboy. I am a discord bot so I am always right.")
        logger.debug(f'Reminded {interaction.user} that fizz is a catboy.')

def setup(bot):
    bot.add_cog(Catboy(bot))
    logger.debug('Setup cog "catboy"')