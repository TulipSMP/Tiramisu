# Tiramisu Style Guide

This document outlines how user-facing messages from the bot should be styled.

## Embeds
Embeds should NEVER be used. They don't fit in with the rest of discord and make the bot's messages 'pop out' and draw attention to itself-- which we don't want.

## Log Messages

### Heading
Messages in the modlog or other kinds of log channels should be headed with a Bold title starting with an emoji and a space, followed by a colon. The title's text should start with the subject followed by the action. For example: 'User Warned', or 'Message Edited'. They should stay as two-word phrases as much as possible.

### Body
The body of the message should contain each field on a new line, a short one or two-word phrase without formatting, followed by a colon, a space, and the content of the field underlined. Additional complex and not readily neccessary information like a user's ID should be covered with a spoiler. Numerical and other non-user-modifiable identifiers should also be in inline code blocks to signify their significance and technical purpose.

### Talking about Users
Users in these messages should be shown by their current display name. Additionally, their username and ID should be in a spoiler as noted above.

## DM messages
Messages sent to DMs should be formatted accordingly:

```markdown
*You have been {ACTIONED} in __{GUILD NAME}__. For:*
>>> {REASON}
```