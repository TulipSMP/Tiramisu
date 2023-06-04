# reporting.py
A cog for slash commands used to report users and bugs.

## Settings
* `modlog_channel`: where to put reports

## Slash Commands
### `/report user`
Reports a user to the mod team

#### Options
* `user`: a `nextcord.Member`, who to report
* `reason`: a `str`, why that user was reporting

### `/report player`
Report a player in the minecraft server

#### Options
* `player`: a `str`, the username of the player to report
* `reason`: a `str`, why they're being reported

### `/report bug`
Report a bug with something in a community's setup or software.

#### Options
* `place`: a `str`, where the bug took place
* `behavior`: a `str`, description of the bug
* `expected`: a `str`, expected behavior
* `reproduce`: a `str`, steps to reproduce

#### Settings
* `bugreports_channel`: where to send bug reports to (required)