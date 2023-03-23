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
        guilds = await self.bot.fetch_guilds(limit=None).flatten()
        logger.info(f'Verifying Database. Guilds: {guilds}')
        for guild in guilds:
            db = Database(guild, reason = f'Verifying database for guild {guild.id} (on start).')
            db.verify()
            if not db.verify(custom='quizzes', check_others=False, check_settings=False):
                with open('config/questions.yml', 'r') as ymlfile:
                    q_config = yaml.load(ymlfile, Loader=yaml.FullLoader)
                if db.create(table=q_config['database']['name'], custom=True, columns=q_config['database']['columns']):
                    logger.success(f'Creates quizzes table for guild {guild.id}!')
                else:
                    logger.error(f'Failed to create quizzes table for guild {guild.id}')
        db.close()
    
    @commands.Cog.listener('on_guild_join')
    async def on_guild_join(self, guild):
        # Create databases on joining a guild
        logger.info(f'Creating database tables for newly joined guild {guild.id}')
        db = Database(guild, reason = f'Creating database for new guild {guild.id}')
        db.create()
        with open('config/questions.yml', 'r') as ymlfile:
                    q_config = yaml.load(ymlfile, Loader=yaml.FullLoader)
        if db.create(table=q_config['database']['name'], custom=True, columns=q_config['database']['columns']):
            logger.success(f'Creates quizzes table for guild {guild.id}!')
        else:
            logger.error(f'Failed to create quizzes table for guild {guild.id}')
        db.close()

    @commands.Cog.listener('on_guild_leave')
    async def on_guild_leave(self, guild):
        logger.info(f'Removing tables for guild {guild.id} on leave!')
        db = Database(guild, reason = f'Deletion upon guild leave')
        db.delete(custom=['quizzes'])
        db.close()

def setup(bot):
    bot.add_cog(Tasks(bot))
    logger.debug('Setup cog "tasks"')