# utilities.py
Simple utilities for members and admins.

## Slash Commands
### `/ip`
Shows a game server IP

##### Settings
* `ip_address`: what address to show
* `ip_text`: a description of the game server, could be used for instructions
* `ip_game`: what game the game server is running

### `/addrole`
Give every user a certain role. Requires the user to be [an admin](/doc/cogs/admin.md)

#### Options
* `role`: a `nextcord.Role`, what role to give everyone

### `/delrole`
Remove a certain role from everyone. Requires the user to be [an admin](/doc/cogs/admin.md)

#### Options
* `role`: a `nextcord.Role`, what role to remove from everyone
