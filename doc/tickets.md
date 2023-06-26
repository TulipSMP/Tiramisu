# Tiramisu's Ticketing System
> *Added in [#39](https://github.com/RoseSMP/Tiramisu/pull/39)*

The ticketing system allows users to speak with moderators privately.


## Procedure
To create a ticket, Tiramisu creates a private thread in the `ticket_channel`, mentioning the `staff_role` and the user who created the ticket to add them to the thread. 

To close a ticket, Tiramisu gets the ticket creator from the original message it sent, and DMs a link to the thread. It then closes and locks the thread, and sends a message about the ticket being closed in the `modlog_channel`.

## `lib/ticketing.py`
The `ticketing` module contains all the functions needed for creating tickets. 

#### *async def **create(interaction: nextcord.Interaction, reason: str = None, buttons: bool = False, require_reason: bool = True)***
Create a Ticket

Parameters:
- `interaction`: the `nextcord.Interaction` to respond to.

Optional:
- `reason`: `str`, the reason for creating the ticket.
- **`NotImplemented:`** `buttons`: `bool`, whether to use buttons in the ticket system
- `require_reason`: `bool`, default `True`, whether to open a modal and ask for a reason if one is not given.


#### *async def **is_ticket(thread: nextcord.Thread or nextcord.Channel, debug: bool = False)***
Check if a Thread is a ticket

This checks that `thread` is a private thread (`nextcord.ChannelType.private_thread`), named `Thread #{int}`, that the ticket number is below the internal ticket count, that it's a child of `ticket_channel`, that we have started counting tickets and that `ticket_channel` is set. (Not in that order)

Parameters:
- `thread`: a `nextcord.Thread` or `nextcord.Channel`, the channel to check if it's a thread or not.

Optional:
- `debug`: whether to return debug information in a tuple with the normal response.

Returns:
- `bool`: if the `thread` given is a ticket.


#### *async def **get_ticket_creator(thread: nextcord.Thread)***
Get the User who created this ticket
This is done by iterating though history near thread creation time (to get the bot's initial message),
and returning the first user mentioned.

NOTE: This does NOT check if this thread is a ticket.

Parameters:
- `thread`: the `nextcord.Thread` of a Ticket to find the creator of.

Returns:
- `nextcord.Member`: the user who created that ticket

#### *async def **close(interaction: nextcord.Interaction)***
Close a Ticket

Checks that the interaction is in a ticket with `is_ticket()`, gets the author from `get_ticket_creator()`. Then, it responds to the interaction, closes and locks the thread, and sends a link to it (with other info) to the ticket creator and in `modlog_channel`.

Parameters:
- `interaction`: the `nextcord.Interaction` to respond to.