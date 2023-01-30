# Guild Settings
#### ⚠️ This feature is still in development! Some features here may not exist yet, or may not be functional in their current state.
Tiramisu is designed to work across multiple servers, each able to configure the bot to work for them. 

## config/settings.yml
While instance settings are saved in `config/config.yml`, a list of settings are saved in `config/settings.yml`. `settings.yml` is checked by various cogs to ensure that their settings are listed there, and if not it is added. 

Here is an example of this file:
```yaml
settings:
  - system_channel: 'id'
  - announcement_channel: 'id'
  - announcement_role: 'id'
  - staff_role: 'id'
  - commands_channel: 'id'
```
Each entry has its name, like `system_channel`, and a type, like `id`. Here are the types of settings that can be set:

* Strings:
    - str
    - string
* Booleans (true/false):
    - bool
    - boolean
    - bit
* IDs (for channels and roles):
    - id

If a type is not found here, it will be set as a string.