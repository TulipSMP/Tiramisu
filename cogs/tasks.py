from logging42 import logger
import nextcord
from nextcord.ext import commands
import yaml
from libs.database import Database

class Tasks(commands.Cog):
    """ This cog is for tasks that must be run on various bot events """
    def __init__(self, bot):
        self.bot = bot
    
    with open("config/config.yml", "r") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
    TESTING_GUILD_ID=cfg["discord"]["testing_guild"]

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        logger.info('Loaded cog hello.py')

    bot = commands.Bot()

    @bot.event
    async def on_ready(self):
        logger.info('Verifying Database...')
        for guild in nextcord.Client.guilds:
            db = Database(guild, reason = f'Verifying database for guild {guild.id} (on start).')
            db.verify()


def setup(bot):
    bot.add_cog(Tasks(bot))
    logger.debug('Setup cog "tasks"')