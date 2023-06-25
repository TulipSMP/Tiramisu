# 
# Tiramisu Discord Bot
# --------------------
# Utility Functions
# 
from logging42 import logger
from typing import Optional
import nextcord
import yaml
import shutil
import sys

with open('config/config.yml') as ymlfile:
    utility_cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

def error_unexpected(error, name='unknown file'):
    """ Returns Appropriate Error Message for sending to user.
    Parameters:
    - `error`: Exception raised
    - `name`=`'unknown file'`: Where the error occured (for log message)
    Returns:
    - `str`: Error message to respond to interaction with """
    logger.error(f"Error in {name}: `{error}`")
    return utility_cfg['messages']['error'].replace('[[error]]', str(error))

def is_mod(user, db_con):
    """ Check if `user` has the `staff_role` as defined in the database. 
    Parameters:
    - `user`: nextcord.User to check permissions for
    - `db_con`: active database connection 
    Returns:
    - `False`: if the user does not have permissions
    - `True`: if the user does have permissions """

    try:
        role = user.get_role(int(db_con.fetch('staff_role')))
    except ValueError:
        role = None
    
    if role == None:
        return False
    else:
        return True

def occurences(string: str, char: str):
    """ Really bad way to do it, but checks how often `char` appears in `string`.
    Parameters:
     - `string`: str, string to check
        - `char`: str, character to check for """
    count = 0
    for i in string:
        if i == char:
            count += 1
    return count

def valid_setting(guild: nextcord.Guild, setting: str, value):
    """ Check if a setting's value is acceptable
    Parameters:
     - `guild`: the current nextcord.Guild, for checking validity of IDs
     - `setting`: str, name of the setting
     - `value`: any, what you want to set it to
    Returns a Tuple:
     - `bool`: whether the value is acceptable
     - `value`: the value as it should be sent to the database, None if it is unacceptable
     - `message`: a message to inform the user about what happened, if an error took place. Otherwise, it's an empty string."""
    with open('config/settings.yml', 'r') as file:
        settings_yml = yaml.load(file, Loader=yaml.FullLoader)
    if setting in settings_yml['settings']:
        try:
            type_name = 'Channel, Role, or User'

            if value == 'none'or value == None:
                return True, 'none', ''
            
            elif setting.endswith('_channel'):
                value = value.strip(' <#>')
                type_name = 'Channel'
                if guild.get_channel(int(value)) != None and value.isdigit():
                    return True, value, ''
                else:
                    return False, None, 'Not a valid channel.'
            
            elif setting.endswith('_role'):
                value = value.strip(' <@&>')
                type_name = 'Role'
                if guild.get_role(int(value)) != None and value.isdigit():
                    return True, value, ''
                else:
                    return False, None, 'Not a valid role.'
            
            elif setting.endswith('_user'):
                value = value.strip(' <@>')
                type_name = 'User'
                if guild.get_user(int(value)) != None and value.isdigit():
                    return True, value, ''
                else:
                    return False, None, 'Not a valid user.'
            
            elif setting.endswith('_address'):
                if occurences(value, '.') >= 2:
                    return True, value, ''
                else:
                    return False, None, 'Not a valid address.'
            
            # Plain-text settings values
            elif setting.endswith('_text') or setting.endswith('_game') or setting.endswith('_name'):
                return True, value.strip(), ''
            else:
                return False, None, 'Unknown setting type.'
        except ValueError:
            return False, None, f'Not a valid {type_name}'
    else:
        return False, None, 'Not a valid setting.'

def verify_config(repair: Optional[bool] = True):
    """ Verify contents of `config/config.yml` against `config/exampleconfig.yml`
    Will repair if `repair` is set to true (default True)
    If `repair` is `None`, it will check the `TIRAMISU_FIX_CONFIG` environment variable first. """
    
    with open('config/config.yml', 'r') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    with open('config/exampleconfig.yml', 'r') as file:
        example = yaml.load(file, Loader=yaml.FullLoader)
    
    missing_paths = []
    def _recurse_check(config: dict, example: dict, path) -> dict:
        missing = {}
        for key in example:
            if key not in config:
                print(f'MISSING: {path}.{key}')
                missing_paths.append(f'{path}.{key}')
                missing[key] = example[key]
            elif type(example[key]) == dict:
                recursed = _recurse_check(config[key], example[key], f'{path}.{key}')
                if recursed != {}:
                    missing[key] = recursed
            else:
                print(f'SUCCESS: {path}.{key}')
        return missing
    
    def _merge(a, b, path=None, update=True):
        """ Merges lists recursively,
        Credit to Andrew Cooke and Osiloke on StackOverflow: https://stackoverflow.com/a/25270947/16263200 """
        if path is None: path = []
        for key in b:
            if key in a:
                if isinstance(a[key], dict) and isinstance(b[key], dict):
                    _merge(a[key], b[key], path + [str(key)])
                elif a[key] == b[key]:
                    pass # same leaf value
                elif isinstance(a[key], list) and isinstance(b[key], list):
                    for idx, val in enumerate(b[key]):
                        a[key][idx] = _merge(a[key][idx], b[key][idx], path + [str(key), str(idx)], update=update)
                elif update:
                    a[key] = b[key]
                else:
                    raise Exception('Conflict at %s' % '.'.join(path + [str(key)]))
            else:
                a[key] = b[key]
        return a

    missing = _recurse_check(config, example, '')
    if missing == {}:
        logger.success(f'Config did not need repaired!')
    elif repair:
        logger.warning(f'Repairing `config/config.yml`. Comments in this file cannot be retained, the original file will be copied to `config/config.yml.old`')
        shutil.copyfile('config/config.yml', 'config/config.yml.old')
        try:
            new = _merge(config, missing)
            with open('config/config.yml', 'w') as file:
                yaml.dump(new, file)
        except:
            shutil.copyfile('config/config.yml.old', 'config/config.yml')
            logger.critical(f'Could not repair `config/config.yml`! You must manually add the following keys: {missing_paths}')
            logger.critical(f'Refer to `config/exampleconfig.yml` for the default values of these entries.')
            sys.exit()
        logger.warning(f'Repaired `config/config.yml`! You should check `config/config.yml` to ensure it was repaired correctly. The old config file was backed up to `config/config.yml`')
        logger.warning(f'Your `config/config.yml` file is now in a strange state: it may not be in the same order, and all comments are missing. Make sure to return it to a human-readable state manually.')
    else:
        logger.critical(f'Your config file is missing the following options: {missing_paths}')
        logger.critical(f'You must add these options to `config/config.yml` manually or copy over `config/exampleconfig.yml` in its place and reconfigure your bot!')
        sys.exit()
        
    