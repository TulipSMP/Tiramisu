# Guild Settings
### ⚠️ This feature is still in development! Some features here may not exist yet, or may not be functional in their current state.
Tiramisu is designed to work across multiple servers, each able to configure the bot to work for them. 

## config/settings.yml
While instance settings are saved in `config/config.yml`, a list of settings are saved in `config/settings.yml`. `settings.yml` is checked by various cogs to ensure that their settings are listed there, and if not it is added. 

Here is an example of this file:
```yaml
settings:
  - 'system_channel'
  - 'announcement_channel'
  - 'announcement_role'
  - 'staff_role'
  - 'server_admin'
  - 'commands_channel'
```

## Database
On the low-level, each guild the bot is in should have a database called `settings_{guild.id}` (where `{guild.id}` is the guild's ID). In this database, there are two columns/values: `setting` and `value`. Both are strings.

Currently each setting can have only one value, and values cannot exceed 255 characters.