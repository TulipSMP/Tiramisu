# mod_rightclick.py
> *Added in [#34](https://github.com/RoseSMP/Tiramisu/pull/34)*

Allows certain moderation actions from `libs.moderation` to be performed via right-clicking users or messages.

To use this, right-click a user or message and go to the *Apps* section of the context menu.

## Message Actions
### Warn For Message
Warns a user for the message that was right-clicked on.

Uses all the default options of `libs.moderation.warn`.

The warn reason contains a link to the message, and the text contents of the message.


## User Actions
### Warn
Warns a user for the given reason.

Uses all the default options of `libs.moderation.warn`.

Opens a `libs.modals.WarnModal` to retrieve the warn reason.

### Kick
Kicks a user for the given reason.

Uses all the default options of `libs.moderation.kick`.

Opens a `libs.modals.KickModal` to retrieve the kick reason.

### Ban
Bans a user for the given reason.

Uses all the default options of `libs.moderation.ban`.

Opens a `libs.modals.BanModal` to retrieve the ban reason.