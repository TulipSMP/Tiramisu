from logging42 import logger
import nextcord
from nextcord.ext import commands
import yaml

class Catboy(commands.Cog):
    def __init__(self, bot):
        self.client = bot
    
    with open("config/config.yml", "r") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
    TESTING_GUILD_ID=cfg["discord"]["testing_guild"]

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        logger.info('Loaded cog catboy.py')

    # Commands
    @nextcord.slash_command(description="Try me!", guild_ids=[TESTING_GUILD_ID])
    async def fizz(self, interaction: nextcord.Interaction):
        await interaction.send(f"Yes, fizz is indeed a catboy. I am a discord bot so I am always right.")
        logger.debug(f'Reminded {interaction.user} that fizz is a catboy.')

def setup(bot):
    bot.add_cog(Catboy(bot))
    logger.debug('Setup cog "catboy"')