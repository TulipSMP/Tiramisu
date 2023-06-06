# Moderation Actions

All moderation actions are run from `libs/moderation.py`. The functions there handle the interaction and everything related except for making sure the user initiating the action has permission to do so. This should be handled by respective slash commands.

Slash commands and other interactions need to check if the user has permissions, then pass the options to the function, awaiting it.

## Functions

### modlog
(async) Sends an alert to the modlog (setting `modlog_channel`). Used internally for following functions.

Parameters:

- `guild`: nextcord.Guild, which guild this message is for
- `subject`: bold heading in messages
- `author`: nextcord.User, who performed the action
- `recipient`: nextcord.User, who the action was performed on
- `additional`: optional dict, added fields for the message
- `reason`: optional str, why this action was performed

Returns:
- `str`: A message about whether this action was successful, to be put in the interaction response message

### kick
(async) Kick `user` and respond to `interaction`.

Parameters:

- `interaction`: nextcord.Interaction for event
- `bot`: the nextcord.User object for this bot
- `user`: nextcord.User to kick
- `reason`: str for why kicked

### timeout
(async) Timeout `user` and respond to `interaction`.

Parameters:
- `interaction`: nextcord.Interaction for event
- `bot`: the nextcord.User object for this bot
- `user`: nextcord.Member to timeout
- `duration`: datetime.datetime or timedelta; how long to time out user
- `reason`: str; why they were timed out

### ban
(async) Ban `user` from `interaction.guild`, and respond to `interaction`:

Parameters:
- `interaction`: nextcord.Interaction for this event
- `bot`: the nextcord.User for this bot
- `user`: the nextcord.Member to ban
- `reason`: why this member was banned 

Optional:
- `dm`: bool, whether to DM the user why they were banned (default True)
- `delete_msgs`: int, 0 - 7, how many days of messages to delete (default 0)

### warn
(async) Warn `user` via DM and/or public message

Parameters:
- `interaction`: nextcord.Interaction for this event
- `bot`: nextcord.User for the bot
- `user`: the nextcord.Member to warn
- `reason`: warn message

Optional:
- `dm`: bool, whether to DM the warn to the user (default True)
- `broadcast`: bool, whether to publicly send the warn in the current channel (default True)

