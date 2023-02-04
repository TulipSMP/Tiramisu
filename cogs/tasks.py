from logging42 import logger
import nextcord
from nextcord.ext import commands
import yaml
from libs.database import Database

class Tasks(commands.Cog):
    """ This cog is for tasks that must be run on various bot events """
    def __init__(self, bot):
        self.bot = bot
        self.client = nextcord.Client()
    
    with open("config/config.yml", "r") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
    TESTING_GUILD_ID=cfg["discord"]["testing_guild"]

    client = nextcord.Client()

    # Events
    @commands.Cog.listener('on_ready')
    async def on_ready(self):
        logger.info('Loaded cog tasks.py')
        # Ensure databases exist for each guild the bot is in
        logger.info('Verifying Database...')
        guilds = [guild.id for guild in self.client.guilds]
        for guild in guilds:
            db = Database(guild, reason = f'Verifying database for guild {guild.id} (on start).')
            db.verify()
    
    @commands.Cog.listener('on_guild_join')
    async def on_guild_join(self, guild):
        # Create databases on joining a guild
        logger.info(f'Creating database tables for newly joined guild {guild.id}')
        db = Database(guild, reason = f'Creating database for new guild {guild.id}')
        db.create()


def setup(bot):
    bot.add_cog(Tasks(bot))
    logger.debug('Setup cog "tasks"')