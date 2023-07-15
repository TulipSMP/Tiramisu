# Tiramisu Moderator Guide
<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/3.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/3.0/80x15.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/3.0/">Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License</a>.

A training manual of sorts for moderators using Tiramisu. It contains all you need to know on how to use Tiramisu's moderation actions


## Slash Commands

Slash commands are the best way to perform moderation actions, as they give you the most control.

### Warn
Warn a user. Usage:
```
/warn user:[Select a User] reason:[Why to warn them] dm:True broadcast:True
```
 * `user`: Select the user to warn
 * `reason`: The reason you are warning them. Sent in warn messages, and in the modlog.
 * `dm`: *Optional, Default `True`*; If enabled, Tiramisu will DM the user the warning message. 
 * `broadcast`: *Optional, Default `True`*; If enabled, Tiramisu will send a warning message in the current channel for all to see.

### Timeout
Trigger the [discord-provided timeout feature](https://support.discord.com/hc/en-us/articles/4413305239191-Time-Out-FAQ). Usage:
```
/timeout user:[Select a User] duration:[Select a Time] reason:["No reason given."]
```
 * `user`: Select the user to timeout
 * `duration`: How long the timeout should last for. Select 'Remove Timeout' instead to remove an existing timeout.
 * `reason`: *Optional, Default `'No reason given.'`*; Why you are timing them out. **NOTE: The reason is currently NOT dmed to the user.**

### Kick
Kick a user. Usage:
```
/kick user:[Select a User] reason:["No reason given."] dm:True
```
 * `user`: Select the user to kick
 * `reason`: *Optional, Default `'No reason given.'`*; Why you are kicking the user.
 * `dm`: *Optional, Default `True`*; If enables, DMs the user the reason before kicking them from the server.

### Ban
Ban a user. Usage:
```
/ban user:[Select a User] reason:[Why to ban them] delete_message_days:["0 days'] dm:True
```
 * `user`: Select a user to ban
 * `reason`: Why you are banning the user
 * `delete_message_days`: *Optional, Default `'0 days'`*; How many days of previous message history to delete
 * `dm`: *Optional, Default `True`*; Whether to DM the provided reason to the user

## Context Menu Actions

Another way to perform some actions is by right-clicking users or messages. This provides less options by may be faster or more useful in some circumstances.

To access these actions, go to the *Apps* section of the context menu (availible via right-clicking).

![The "Apps" section of the context menu](/src/context-menu-apps.png)


### Message Actions

Actions available via right-clicking a message.

Demo:

![Warning a user for their message via context-menu](/src/context-menu-warn-message.gif)

#### Warn For Message

Quickly warns a user because of a message they sent. Links to the message and shows part of its text content.


### User Actions

Actions available by right-clicking a user.

Demo:

![Warning user via context-menu](/src/context-menu-warn.gif)

#### Ban

Ban a user as normal. A modal pops up for you to enter the ban reason. The optional fields use their defaults as specified above.

#### Kick 

Kick a user as normal. A modal pops up for you to enter the kick reason. The optional fields will use their defaults as specified above.

#### Warn

Warn a user as normal. A modal pops up for you to enter the warn reason. The optional fields will use their defaults as specified above.

## The Modlog

The modlog (short for Moderator's Log) is a channel where Tiramisu reports all moderation actions it performs. This allows for moderators to stay up to date on what others in their team are doing. 

Have an administrator set the `modlog_channel` setting to an appropriate channel to start seeing logs.