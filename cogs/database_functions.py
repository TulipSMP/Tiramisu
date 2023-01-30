from logging42 import logger
import nextcord
from nextcord.ext import commands
import yaml
import mysql.connector
import sqlite3

class Database(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Load Yaml
    # Instance Config
    with open("config/config.yml", "r") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
    # What settings each guild should be able to load
    with open("config/settings.yml", "r") as ymlfile:
        settings = yaml.load(ymlfile, Loader=yaml.FullLoader)

    # Database
    logger.debug("Logging into DB from database.py")
    if cfg["storage"] == "sqlite":
        sql = sqlite3.connect('storage.db')
        cursor = sql.cursor()
    else:
        sql = mysql.connector.connect(
            host=cfg["mysql"]["host"],
            user=cfg["mysql"]["user"],
            password=cfg["mysql"]["pass"],
            database=cfg["mysql"]["db"]
        )
        cursor = sql.cursor()

    # Functions
    # Creates tables for DB
    @logger.catch
    def guild_tables_create(self, guild, table=None):
        if table == 'admins' or table == None:
            self.cursor(f'CREATE TABLE IF NOT EXISTS admins_{guild.id} ( id int, admin bit );')
            logger.info(f'Created table "admins_{guild.id}", if it doesnt already exist!')
        if table == 'settings' or table == None:
            self.cursor(f'CREATE TABLE IF NOT EXISTS settings_{guild.id} ( setting string, value string );')
            for setting in settings['settings']:
                self.cursor(f'INSERT INTO settings_{guild.id} ( setting, enabled ) VALUES ( {setting}, none );')
            logger.info(f'Created table "settings_{guild.id}", if it doesnt already exist!')
    # Fetch information from DB
    # Default to settings if no table is specified
    @logger.catch
    def guild_tables_fetch(self, guild, setting):
        if setting == None or setting == 'admin':
            self.cursor(f'SELECT id FROM admins_{guild.id} WHERE admin=1;')
            return self.cursor.fetchall()
        else:
            self.cursor(f'SELECT enabled FROM admins_{guild.id} WHERE admin=1;')
            return self.cursor.fetchall()
    # Change information in DB
    # Should ALWAYS return true if successfull, false if an error occurred
    @logger.catch
    def guild_tables_set(self, guild, setting, value, clear=False):
        if setting == 'admin' and clear == True:
            try:
                self.cursor(f'DELETE FROM admins_{guild.id} WHERE id IS {value}')
                logger.debug(f'Removed id {value} from table admins_{guild.id}')
                return True
            except:
                logger.warning(f'Failed to delete ID {value} from table admins_{guild.id}!')
                return False
        if setting == 'admin' and clear == False:
            try:
                self.cursor(f'INSERT INTO admins_{guild.id} ( id, admin ) VALUES ( {value}, 1 )')
                logger.debug(f'Added id {value} to table admins_{guild.id}')
                return True
            except:
                logger.debug(f'Failed to add id {value} to table admins_{guild.id}!')
                return False
        
def setup(bot):
    bot.add_cog(Database(bot))
    logger.debug('Setup library "database"')