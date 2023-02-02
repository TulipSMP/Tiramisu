from logging42 import logger
import nextcord
from nextcord.ext import commands
import yaml
import mysql.connector 
import sqlite3

class Database:
    # Connects to Database to fetch/edit settings and other values
    def __init__(self, cursor, guild):
        self.cursor = cursor
        self.guild = guild

    # Load Yaml
    with open("config/config.yml", "r") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
    logger.info(f'CONFIG.yml:\n{cfg}')
    with open("config/settings.yml", "r") as ymlfile:
        settings = yaml.load(ymlfile, Loader=yaml.FullLoader)

    # Functions
    # Creates tables for DB
    @logger.catch
    def guild_tables_create(self, table=None):
        if table == 'admins' or table == None:
            self.cursor(f'CREATE TABLE IF NOT EXISTS admins_{self.guild.id} ( id int, admin bit );')
            logger.info(f'Created table "admins_{self.guild.id}", if it doesnt already exist!')
        if table == 'settings' or table == None:
            with open("config/settings.yml", "r") as ymlfile:
                settings = yaml.load(ymlfile, Loader=yaml.FullLoader)
            self.cursor(f'CREATE TABLE IF NOT EXISTS settings_{self.guild.id} ( setting string, value string );')
            for setting in settings['settings']:
                self.cursor(f'INSERT INTO settings_{self.guild.id} ( setting, enabled ) VALUES ( {setting}, none );')
            logger.info(f'Created table "settings_{self.guild.id}", if it doesnt already exist!')
    # Fetch information from DB
    # Default to settings if no table is specified
    @logger.catch
    def guild_tables_fetch(self, setting):
        if setting == None or setting == 'admin':
            self.cursor(f'SELECT id FROM admins_{guild.id} WHERE admin=1;')
            return cursor.fetchall()
        else:
            self.cursor(f'SELECT enabled FROM settings_{guild.id} WHERE setting={setting};')
            return cursor.fetchall()
    # Change information in DB
    # Should ALWAYS return true if successfull, false if an error occurred
    @logger.catch
    def guild_tables_set(cursor, guild, setting, value, clear=False):
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

    # Events
    @bot.event
    async def on_ready(self):
        logger.info('Loaded cog database_functions.py')
    @bot.event
    async def on_guild_join(self, guild):
        pass
        #db.guild_tables_create(self.cursor, guild)

def setup(bot):
    bot.add_cog(Database(bot))
    logger.debug('Setup cog "database_functions"')