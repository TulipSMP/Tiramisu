# moderation.py
A cog for most moderation actions. Like warn, ban, etc.

## Slash commands
### `/warn`
Warn a user. Sends a DM and a message in chat by default.

#### Options
* `user`: a `nextcord.Member`, who to warn
* `reason`: a `str`, why they were warned
* `show_message`: a `bool`, whether to also show a message in chat (default `True`)