# announce.py
Actually quite a simple cog, just for sending announcements.

It uses the `announcement_channel` setting to get where to send announcements, and the `announcement_role` setting to get the role to ping if the `ping` option is set to true.

## Slash commands
### `/announce`
Sends an annoucement to a configured channel, optionally pinging an annoucement role. Requires the `announcement_channel` setting to be set.

#### Options
* `announcement`: a `str`, what to say in the announcement 
* `ping`: a `bool`, whether to ping the `announcement_role`
