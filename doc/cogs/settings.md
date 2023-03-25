# settings.py
A cog for the slash commands to change guild settings. Main page: [guild-settings.md](/doc/guild-settings.md).

## Slash Commands
### `/setting get`
Get what a setting is currently set to.

#### Options
* `setting`: a `str`, which setting to fetch
    - if `all` is passed, a list of all settings is returned instead

### `/setting set`
Change a setting

#### Options
* `setting`: a `str`, what setting to change
* `value`: a `str`, what to change the setting to