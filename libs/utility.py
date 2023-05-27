# 
# Tiramisu Discord Bot
# --------------------
# Utility Functions
# 
from logging42 import logger
import nextcord

async def error_unexpected(interaction, error, name='unknown file'):
    """ Respond with an error message because of an Uncaught or Unexpected Error """
    logger.error(f"Error in {name}: {error}")
    await interaction.send(self.cfg['messages']['error'].replace('[[error]]', str(error)), ephemeral=True)

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