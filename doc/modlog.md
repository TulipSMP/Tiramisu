# The Mod Log

Tiramisu logs most moderation-related actions in the modlog.

## Database

Most of the moderator-performed actions are sent to a DB.

Here is a db example:

timestamp | uuid | action | moderator | recipient | reason | extra
----------|------|--------|-----------|-----------|--------|----------
032342433424| 888f89-897897f-897sd897f-001123 | kick | 897327483758943 | 834754365743| bad word smh | {"Evidence":"https://cdn.discordapp.com/43534564645645/546456546.webm"}

### Values:

- `timestamp`: time of action in unix millis
- `uuid`: a uuid for the event (currently unused)
- `action`: what was done, can be one of:
    - kick
    - ban
    - timeout
    - warn
- `moderator`: discord ID of the moderator to perform the action
- `recipient`: either a discord id or a minecraft username of who the action was performed on
- `reason`: the reason the action was performed
- `extra`: json of extra fields, if any. 
