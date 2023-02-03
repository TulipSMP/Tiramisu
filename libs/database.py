from logging42 import logger
import yaml
import itertools

class Database:
    """ Fetch & Write information from Database """
    def __init__(self, guild, reason='No Reason Specified'):
        self.guild = guild
        self.reason = reason
        # Load Yaml
        with open("config/config.yml", "r") as ymlfile:
            self.cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
        with open("config/settings.yml", "r") as ymlfile:
            self.settings = yaml.load(ymlfile, Loader=yaml.FullLoader)
        # Connect to Database
        if self.cfg["storage"] == "sqlite":
            import sqlite3
            sql = sqlite3.connect('storage.db')
            self.cursor = sql.cursor()
            self.db_type = 'sqlite'
        else:
            import mysql.connector
            sql = mysql.connector.connect(
                host=cfg["mysql"]["host"],
                user=cfg["mysql"]["user"],
                password=cfg["mysql"]["pass"],
                database=cfg["mysql"]["db"]
            )
            self.cursor = sql.cursor()
            self.db_type = 'mysql'
        logger.debug(f'Initiated connection to {self.db_type} database for {self.reason}.')

    # Functions
    # Create database tables
    @logger.catch
    def create(self, table=None):
        """ Create Tables for Database required for every guild """
        if table == 'admins' or table == None:
            self.cursor.execute(f'CREATE TABLE IF NOT EXISTS admins_{self.guild.id} ( id int, admin bit );')
            logger.info(f'Created table "admins_{self.guild.id}", if it doesnt already exist!')
        if table == 'settings' or table == None:
            self.cursor.execute(f'CREATE TABLE IF NOT EXISTS settings_{self.guild.id} ( setting string, value string );')
            for setting in self.settings['settings']:
                self.cursor.execute(f'INSERT INTO settings_{self.guild.id} ( setting, enabled ) VALUES ( {setting}, none );')
            logger.info(f'Created table "settings_{self.guild.id}", if it doesnt already exist!')
    # Verify database exists and is correctly setup
    @logger.catch
    def verify(self, tables=True, values=False, create=False):
        if tables:
            existing = self.cursor.execute('show tables;')
            if f'admins_{self.guild.id}' in existing:
                admins_exists = True
            if f'settings_{self.guild.id}' in existing:
                settings_exists = True
        if values:
            settings_absent = []
            amend_settings = False
            tup = self.cursor.execute(f'SELECT setting FROM settings_{self.guild.id};').fetchall()
            existing = list(itertools.chain(*tup))
            for setting in existing:
                if setting in existing:
                    pass
                else:
                    amend_settings = True
                    settings_absent.append(setting)
            if amend_settings:
                for setting in settings_absent:
                    self.cursor.execute(f'INSERT INTO settings_{self.guild.id} ( setting, enabled ) VALUES ( {setting}, none )')

    # Fetch information from DB
    # Default to settings if no table is specified
    @logger.catch
    def fetch(self, setting, return_list=False, admin=False):
        """ Fetch information from Database """
        if admin:
            if return_list:
                tup = self.cursor.execute(f'SELECT id FROM admins_{self.guild.id} WHERE admin=1;').fetchall()
                return list(itertools.chain(*tup))
            else:
                return self.cursor.execute(f'SELECT id FROM admins_{self.guild.id} WHERE id={setting};').fetchone()
        else:
            self.cursor.execute(f'SELECT enabled FROM settings_{self.guild.id} WHERE setting={setting};')
            if return_list:
                tup = self.cursor.fetchall()
                return list(itertools.chain(*tup))
            else:
                return self.cursor.fetchone()

            
    # Change information in DB
    # Should ALWAYS return true if successfull, false if an error occurred
    @logger.catch
    def set(self, setting, value, clear=False):
        """ Set values within the Database
        If value is None, an admin will be removed or a setting will be set to none """
        if setting == 'admin' and clear == True:
            try:
                self.cursor.execute(f'DELETE FROM admins_{self.guild.id} WHERE id IS {value}')
                logger.debug(f'Removed id {value} from table admins_{self.guild.id}')
                return True
            except:
                logger.warning(f'Failed to delete ID {value} from table admins_{self.guild.id}!')
                return False
        elif setting == 'admin':
            try:
                self.cursor.execute(f'INSERT INTO admins_{self.guild.id} ( id, admin ) VALUES ( {value}, 1 )')
                logger.debug(f'Added id {value} to table admins_{self.guild.id}')
                return True
            except:
                logger.warning(f'Failed to add id {value} to table admins_{self.guild.id}!')
                return False
        elif clear == True:
            try:
                self.cursor.execute(f"UPDATE settings_{self.guild.id} SET enabled = (CASE WHEN setting = '{setting}' THEN enabled = 'none'")
                logger.debug(f'Set {setting} to {value} for table settings_{self.guild.id}')
                return True
            except:
                logger.warning(f'Failed to set value {setting} to {value} for table settings_{self.guild.id}!')
                return False
        else:
            try:
                self.cursor.execute(f"UPDATE settings_{self.guild.id} SET enabled = (CASE WHEN setting = '{setting}' THEN enabled = '{value}'")
                logger.debug(f'Set {setting} to {value} for table settings_{self.guild.id}')
            except:
                logger.warning(f'Failed to set value {setting} to {value} for table settings_{self.guild.id}!')
                return False