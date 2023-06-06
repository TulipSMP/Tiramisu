# 
# Tiramisu Discord Bot
# --------------------
# Utility Functions
# 
from logging42 import logger
import nextcord
import yaml

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

            if value == 'none':
                return True, value, ''
            
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
                return True, value.strip()
            else:
                return False, None, 'Unknown setting type.'
        except ValueError:
            return False, None, f'Not a valid {type_name}'
    else:
        return False, None, 'Not a valid setting.'