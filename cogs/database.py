from logging42 import logger
import nextcord
from nextcord.ext import commands
import yaml
import mysql.connector
import sqlite3
from database_functions import DatabaseFunctions as db

class Database(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Load Yaml
    with open("config/config.yml", "r") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
    logger.info(f'CONFIG.yml:\n{cfg}')
    # Load instance owner from yaml
    botowner = cfg["discord"]["owner"]

    # Test guild ID
    TESTING_GUILD_ID=cfg["discord"]["testing_guild"]

    # Database
    logger.debug("Logging into DB from database.py")
    if cfg["storage"] == "sqlite":
        sql = sqlite3.connect('storage.db')
        cursor = sql.cursor()
    else:
        import mysql.connector
        sql = mysql.connector.connect(
            host=cfg["mysql"]["host"],
            user=cfg["mysql"]["user"],
            password=cfg["mysql"]["pass"],
            database=cfg["mysql"]["db"]
        )
        cursor = sql.cursor()

    # Events
    @bot.event
    async def on_ready(self):
        logger.info('Loaded cog admin.py')
    @bot.event
    async def on_guild_join(self, guild):
        db.guild_tables_create(self.cursor, guild)

def setup(bot):
    bot.add_cog(Database(bot))
    logger.debug('Setup cog "database"')