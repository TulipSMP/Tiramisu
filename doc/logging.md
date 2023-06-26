# Action Logging
> *Added in [#41](https://github.com/RoseSMP/Tiramisu/pull/41)*

In order to assist moderators, Tiramisu logs certain member actions.

This logging is sent to `log_channel`.

## Sending a log message
To send a log message, you must first have a `libs.logging.LoggingEvent` that pertains to the event that happened (these are available in `libs/logging.py`).

Then, that object is passed to `libs.logging.log()`. That function uses 3 attributes from the `event`:
- `.guild`: the `nextcord.Guild` this event happened in
- `.void`: a `bool`, if true this event will not be logged
- `.message()`: a function that should return a `str` to be sent to the `log_channel`.

## Available LoggingEvents:

### *LoggingEvent(guild: nextcord.Guild, title: str, user: nextcord.User, extra: dict = {})*
Base class for logging events

Parameters:
- `guild`: nextcord.Guild, the guild this is happening in
- `title`: str, the heading for the log message
- `user`: nextcord.User, the doer of the action
- `extra`: optional dict, fields for the message

### *DeletedMessage(message: nextcord.Message)*
Event for a message being deleted

Parameters:
- `message`: the `nextcord.Message` that was deleted


### *EditedMessage(old: nextcord.Message, new:nextcord.Message)*
Event for message being edited

Parameters:
- `old`: the `nextcord.Message` before editing
- `new`: the `nextcord.Message` after editing

### *ChangeVoice(member: nextcord.Member, before: nextcord.VoiceState, after: nextcord.VoiceState)*
Event for Voice state update

Parameters:
- `member`: the `nextcord.Member` whose VoiceState has changed
- `before`: the `nextcord.VoiceState` before the change
- `after`: the `nextcord.VoiceState` after the change

