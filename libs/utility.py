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

async def error_unexpected(error, name='unknown file'):
    """ Returns Appropriate Error Message for sending to user.
    Parameters:
    - `error`: Exception raised
    - `name`=`'unknown file'`: Where the error occured (for log message)
    Returns:
    - `str`: Error message to respond to interaction with """
    logger.error(f"Error in {name}: {error}")
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