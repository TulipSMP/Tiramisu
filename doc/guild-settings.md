# Guild Settings
Guild settings are how Tiramisu stores a guild's settings for the bot. As in channels, roles, etc. that are allowed to access certain permissions. These settings are stored in an SQL database, easily set and accessed via `libs/database.py`.

## Available settings
Settings that the user can change are listed under the `settings:` key in `config/settings.yml`. Whenever the bot starts, or a new guild is joined, appropriate tables are created. These are promptly deleted when the bot leaves a guild. 

## Changing settings
Settings are changed via the `/setting set` slash command, and their values can be checked with the `/setting get` command. A list of all available settings can be fetched with `/setting get` with the setting `all` (which is not an actual setting).

This slash command uses the `db.set()` method to change settings.

## Using settings
### Prerequisites
In order to have your cog access a setting, the setting's name must first be listed under `settings:` in `config/settings.yml` on start of the bot.
Next, you must import the `Database()` class from `libs/database.py`, like so:
```python
from libs.database import Database
```
### Connecting to the Database
Whenever you need to access the database connect to it first, like so (a new connection must be established for each different guild):
```python
db = Database(guild)
```
NOTE: `guild` must be a guild object, NOT a guild ID. The library internally gets the ID from the `guild` object. 
You may optionally specify the `reason` parameter, to show in the log *why* you initiated a database connection, like so:
```python
db = Database(guild, reason='Slash command `/ip`')
```
### Fetching your settings from the database
After the above is complete, fetching values is quite simple:
```python
your_value = db.fetch('your_setting')
```
As SQL columns define each variable type for the whole column, settings are stored (and thus returned) as strings. If not set, the default value is the string `'none'`. Also, variable types are not checked. Your code should handle errors changing your setting's value to what you need, and tell the user to change the appropriate setting to a valid value (which you should specify). If your feature requires that the setting be set (i.e. has no default) it should inform the user that the admins have not set up this feature, and that they should change that setting to the type you need.

### Changing settings
If you want to change a setting for some reason, use the `.set()` method:
```python
db.set('your_setting', 'your_value')
```
You should ALWAYS call the `.close()` method, which saves changes to the database if it's using `sqlite`.
```python
db.close()
```

## Type Hinting
Inferred from the last part of a setting's name are types of settings (referred to as suffixes). If the user sets a setting to an unacceptable value, they are warned in the response message (but the value is currently still set). Additionally, types that are IDs strip the characters used in mentioning them from the input value, so that just the ID is saved to the database. This way, users can set channel, role, etc. settings without having to find the ID. The table below outlines different types and how they are handled:

| Type  | Suffix | Characters Removed | Checks |
|-------|--------|-------|--------|
| Channel | `_channel` | ` <#>` | `self.bot.get_channel(value) != None` |
| Role  | `_role` | ` <@&>` | `interaction.guild.get_role(value) != None` |
| User | `_user` | ` <@>` | `self.bot.get_user(value) != None` |
| Address | `_address` | None | `self.occurs(value, '.') >= 2` |

## Database
On the low-level, each guild the bot is in has a table called `settings_{guild.id}` (where `{guild.id}` is the guild's ID). In this database, there are two columns/values: `setting` and `value`. Both are strings. This is checked whenever the bot starts, and tables are created whenever the bot joins a new guild.

Currently each setting can have only one value, and values cannot exceed 255 characters.