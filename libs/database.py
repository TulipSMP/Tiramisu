from logging42 import logger
import yaml
import itertools
import sys

class Database:
    """ Fetch & Write information to/from from Database """
    def __init__(self, guild, reason='No Reason Specified'):
        self.guild = guild
        self.reason = reason
        # Load Yaml
        with open("config/config.yml", "r") as ymlfile:
            self.cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
        with open("config/settings.yml", "r") as ymlfile:
            self.settings = yaml.load(ymlfile, Loader=yaml.FullLoader)
        if self.cfg['storage'] == 'sqlite':
            self.connect('init')
        
        if type(self.guild) == type(100):
            logger.critical(f'Database() should be invoked with a Guild() object, not a guild id!')
            sys.exit(2)

    # Functions
    # Connect to DB
    @logger.catch
    def connect(self, subreason):
        # Connect to Database
        if self.cfg["storage"] == "sqlite":
            import sqlite3
            sql = sqlite3.connect('storage.db')
            self.sql = sql
            self.cursor = sql.cursor()
            self.db_type = 'sqlite'
            self.current_database = sqlite3
        elif self.cfg["storage"] == "mysql":
            import mysql.connector
            sql = mysql.connector.connect(
                host=self.cfg["mysql"]["host"],
                user=self.cfg["mysql"]["user"],
                password=self.cfg["mysql"]["pass"],
                database=self.cfg["mysql"]["db"]
            )
            self.cursor = sql.cursor()
            self.db_type = 'mysql'
            self.current_database = mysql
        else:
            logger.critical('Invalid storage type! Please edit the "storage" option in config/config.yml to either "mysql" or "sqlite" depending on which database you intend to use.')
            sys.exit(1)
        logger.info(f'Connected to {self.db_type} database in {subreason} for {self.reason}')
    # Create database tables
    @logger.catch
    def create(self, table=None, custom=False, columns=None):
        """ Create Tables for Database required for every guild """
        if self.cfg['storage'] == 'mysql':
            self.connect('create')
        if table == 'admins' or table == None:
            self.cursor.execute(f'CREATE TABLE IF NOT EXISTS "admins_{self.guild.id}" ( id int, admin bit );')
            if self.db_type == 'sqlite':
                self.sql.commit()
            logger.info(f'Created table "admins_{self.guild.id}", if it doesnt already exist!')
        if table == 'settings' or table == None:
            self.cursor.execute(f'CREATE TABLE IF NOT EXISTS settings_{self.guild.id} ( setting string, value string );')
            for setting in self.settings['settings']:
                self.cursor.execute(f'INSERT INTO settings_{self.guild.id} ( setting, value ) VALUES ( "{setting}", "none" );')
            if self.db_type == 'sqlite':
                self.sql.commit()
            logger.info(f'Created table "settings_{self.guild.id}", if it doesnt already exist!')
        if custom:
            if type(columns) != type(str([1,2,3])) or table == None:
                logger.critical(f'A custom table was passed but it was not described correctly!')
            else:
                columns_string = ''
                for item in columns:
                    columns_string += f' {item},'
                if columns_string.endswith(','):
                    columns_string = columns_string.removesuffix(',')
                self.cursor.execute(f'CREATE TABLE IF NOT EXISTS "{table}_{self.guild.id}" ({columns_string} );')
    
    # Verify Databases
    @logger.catch
    def verify(self, custom=None, check_others=True):
        """ Verify admins_* and settings_* table, or custom tables, for a certain guild """
        if self.cfg['storage'] == 'mysql':
            self.connect('verify')
        # Fetch list of tables
        if self.db_type == 'sqlite':
            table_list = self.cursor.execute(f'select name from sqlite_schema where type="table" and name not like "sqlite_%";').fetchall()
        elif self.db_type == 'mysql':
            table_list = self.cursor.execute(f'select * from information_schema.tables;').fetchall()
        table_list = list(itertools.chain(*table_list))
        # Check if tables exist, and print success to log
        table_check = ['admins', 'settings']
        if custom != None:
            if not check_others:
                table_check = []
            if type(custom) == type(['li','st']):
                for item in custom:
                    table_check.append(item)
            else:
                table_check.append(custom)
        table_repair = []
        for table in table_check:
            if f'{table}_{self.guild.id}' in table_list:
                logger.success(f'{table}_{self.guild.id} found during DB verification!')
            else:
                logger.warning(f'{table}_{self.guild.id} was not found during DB verification!')
                table_repair.append(table)
        # If a table is missing, create it
        for table in table_repair:
            self.create(table)
            logger.warning(f'Table {table}_{self.guild.id} did not exist, so it was created.')
        # Fetch list of necessary settings
        with open('config/settings.yml') as settings_yml:
            settings = yaml.load(settings_yml, Loader=yaml.FullLoader)
        # Fetch existing settings from database
        settings_existing = self.cursor.execute(f'select setting from "settings_{self.guild.id}";').fetchall()
        settings_existing = list(itertools.chain(*settings_existing))
        # Check what settings are missing
        settings_missing = []
        for setting in settings['settings']:
            if setting in settings_existing:
                pass
            else:
                settings_missing.append(setting)
        # if setting is missing, create it
        for setting in settings_missing:
            self.cursor.execute(f'insert into "settings_{self.guild.id}" ( setting, value ) values ( "{setting}", "none" );')
        logger.success(f'Added settings {settings_missing} to table settings_{self.guild.id} because they did not exist!')

    # Fetch information from DB
    # Default to settings if no table is specified
    @logger.catch
    def fetch(self, setting, admin=False, verifying_settings=False, custom=False, table=None, setting_row=None, select_row=None,
        fetchall=False):
        """ Fetch information from Database 
        To access a custom table, the following optional parameters must be specified:
            - custom=True
            - setting_row (to check for `setting` in sql select)
            - select_row (the row to return output from) 
            - setting (what to check for in setting_row in sql select. should be a unique identifier)"""
        if self.cfg['storage'] == 'mysql':
            self.connect('fetch')
        if admin or setting == 'admins':
            try:
                tup = self.cursor.execute(f'SELECT * FROM "admins_{self.guild.id}";').fetchall()
            except self.current_database.OperationalError:
                self.create()
                tup = self.cursor.execute(f'SELECT * FROM "admins_{self.guild.id}";').fetchall()
            admin_list = list(itertools.chain(*tup))
            for item in admin_list:
                if item == 1:
                    admin_list.remove(1)
            return admin_list
        elif custom and table != None and setting_row != None and select_row != None:
            logger.debug(f'Accessing custom table {table}_{self.guild.id}.')
            try:
                statement = f'SELECT "{select_row}" FROM "{table}_{self.guild.id}" WHERE {setting_row}="{setting}"'
                if fetchall:
                    tup = self.cursor.execute(statement).fetchall()
                    return list(f"[{tup.replace('(', '').replace(')', '')}]")
                else:
                    tup = self.cursor.execute(statement).fetchone()
                    return str(tup).replace('(', '').replace(')', '').replace("'", '').replace(',', '')
            except self.current_database.OperationalError:
                return False
        else:
            if verifying_settings:
                if setting in self.cursor.execute(f'SELECT setting FROM "settings_{self.guild.id}" WHERE setting="{setting}"').fetchall():
                    return True
                else:
                    return False
            else:
                tup = self.cursor.execute(f'SELECT value FROM "settings_{self.guild.id}" WHERE setting="{setting}";').fetchone()
                return str(tup).replace('(', '').replace(')', '').replace("'", '').replace(',', '')

            
    # Change information in DB
    # Should ALWAYS return true if successfull, false if an error occurred
    @logger.catch
    def set(self, setting, value, clear=False):
        """ Set values within the Database. Returns true if successful.
        If value is None, an admin will be removed or a setting will be set to none """
        if self.cfg['storage'] == 'mysql':
            self.connect('set')
        if setting == 'admin' and clear == True:
            try:
                self.cursor.execute(f'DELETE FROM admins_{self.guild.id} WHERE id IS {value}')
                logger.info(f'Removed id {value} from table admins_{self.guild.id}')
                return True
            except:
                logger.warning(f'Failed to delete ID {value} from table admins_{self.guild.id}!')
                return False
        elif setting == 'admin':
            try:
                self.cursor.execute(f'INSERT INTO admins_{self.guild.id} ( id, admin ) VALUES ( {value}, 1 )')
                logger.info(f'Added id {value} to table admins_{self.guild.id}')
                return True
            except:
                logger.warning(f'Failed to add id {value} to table admins_{self.guild.id}!')
                return False
        elif clear == True:
            try:
                self.cursor.execute(f'UPDATE "settings_{self.guild.id}" SET value="{value}" WHERE setting="none"')
                logger.info(f'Set {setting} to {value} for table settings_{self.guild.id}')
                return True
            except:
                logger.warning(f'Failed to set value {setting} to {value} for table settings_{self.guild.id}!')
                return False
        else:
            try:
                self.cursor.execute(f'UPDATE "settings_{self.guild.id}" SET value="{value}" WHERE setting="{setting}"')
                logger.info(f'Set {setting} to {value} for table settings_{self.guild.id}')
                return True
            except:
                logger.warning(f'Failed to set value {setting} to {value} for table settings_{self.guild.id}!')
                return False
    
    # Send raw commands to Database
    @logger.catch
    def raw(self, command, fetchall=True, fetchone=False):
        """ Send a raw SQL query to the SQL server 
        remember to use the correct table, admins_{self.guild.id} or settings_{self.guild.id}
        Options: fetchall - use `.fetchall()` method and return result (default True)
                 fetchone - use `.fetchone()` method and return result (default False)
                 If both are false, execute bare command and return true if successful """
        if self.cfg['storage'] == 'mysql':
            self.connect('raw')
        try:
            if fetchone:
                return self.cursor.execute(command).fetchone()
            elif fetchall:
                return self.cursor.execute(command).fetchall()
            else:
                self.cursor.execute(command)
                return True
        except self.current_database.OperationalError:
            logger.warning(f'OperationalError when running raw command: "{command}"!')
            return False
    
    # Delete tables of a guild
    @logger.catch
    def delete(self, settings=True, admins=True, custom=None):
        """ Completely delete a guild's data """
        if self.cfg['storage'] == 'mysql':
            self.connect('delete')
        if settings:
            self.cursor.execute(f'drop table "settings_{self.guild.id}";')
            logger.debug(f'Deleted table settings_{self.guild.id}.')
        if admins:
            self.cursor.execute(f'drop table "admins_{self.guild.id}";')
            logger.debug(f'Deleted table admins_{self.guild.id}')
        if custom != None:
            self.cursor.execute(f'drop table "{custom}_{self.guild.id}";')
            logger.debug(f'Deleted custom table {custom}_{self.guild.id}.')
        return True


    # Properly close DB
    @logger.catch
    def close(self):
        """ Close the Database, if necessary """
        if self.db_type == 'sqlite':
            self.sql.commit()
            self.sql.close()
            logger.debug(f'Closed sqlite3 database connection reasoned "{self.reason}".')
            return True
        else:
            return True