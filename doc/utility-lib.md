# Utility Library
`libs/utility.py` contains various utilities for repeated commands that are reused in Tiramisu. It should be added to whenever a code snippet will need to be used in multiple different places across cogs, or it just makes sense to separate it somewhere else.

## Functions

### error_unexpected
Returns Appropriate Error Message for sending to user, when we encounter an error we aren't prepared for. 

Parameters:
- `error`: Exception raised
- `name`=`'unknown file'`: Where the error occured (for log message)

Returns:
- `str`: Error message to respond to interaction with

### is_mod
Check if `user` has the `staff_role` as defined in the database. 

Parameters:
- `user`: nextcord.User to check permissions for
- `db_con`: active database connection 

Returns:
- `False`: if the user does not have permissions
- `True`: if the user does have permissions

### occurences
Really bad way to do it, but checks how often `char` appears in `string`.

Parameters:
- `string`: str, string to check
- `char`: str, character to check for

### valid_setting
Check if a setting's value is acceptable

Parameters:
- `guild`: the current nextcord.Guild, for checking validity of IDs
- `setting`: str, name of the setting
- `value`: any, what you want to set it to

Returns a Tuple:
- `bool`: whether the value is acceptable
- `value`: the value as it should be sent to the database, None if it is unacceptable
- `message`: a message to inform the user about what happened, if an error took place. Otherwise, it's an empty string.