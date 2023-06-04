# admin.py
The `admin` cog is used to save and load guild administrators. These administrators can change settings for the bot, and perform moderation actions.

## Slash Commands
A list of slash commands provided by this cog and what they do.

### `/admin add`
Adds an administrator. Any admin can add administrators, as well as a server's owner.

#### Options
* `user`: a `nextcord.Member`, who to make an administrator.

### `/admin list`
Lists administrators. Can be used by any administrator.

### `/admin rm`
Removes an administrator.

#### Options
* `user`: a `nextcord.Member`, who to revoke administratorship from.
* `mention_user`: a `bool`, whether to ping the `user` in the response (optional)

## For Developers
### How admins are stored
Admins are stored in a database table, similar to how settings are. This cog utilises the same library `libs/database.py` as settings, which can also handle setting and changing admins. 

Admins are stored in the database by their ID.