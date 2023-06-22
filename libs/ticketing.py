# 
# Tiramisu Discord Bot
# --------------------
# Ticketing System
# 
import nextcord
import random

from libs import utility, modals, buttons, moderation
from libs.database import Database

"""
TODO
- [ ] Via slash commands
- [ ] Via a button

- [ ] Create ticket
- [ ] Close ticket


"""
async def create(interaction: nextcord.Interaction, reason: str = None, buttons: bool = False, require_reason: bool = True):
    """ Create a Ticket """
    if reason == None and require_reason:
        await interaction.response.send_modal(modals.InputModal('Create a Ticket', 'Topic of ticket', create)) # Call create again with reason
        return
    elif interaction.channel.type != nextcord.ChannelType.text:
        await interaction.response.send_message('I cannot create tickets here!')
        return

    db = Database(interaction.guild, reason='Ticketing, creating ticket')
    try:
        channel = interaction.guild.get_channel(int(db.fetch('ticket_channel')))
        if channel == None:
            raise ValueError
    except:
        await interaction.send(f'Tickets are not enabled!\n*To enable them, have and admin set the `ticket_channel` setting to an appropriate channel.*')
        return

    ticket_number = db.fetch('ticket_int')
    if ticket_number == 'none':
        ticket_number = 0
    elif ticket_number.isdigit():
        ticket_number = int(ticket_number)
    else:
        ticket_number = 0
    ticket_number += 1
    db.set('ticket_int', str(ticket_number))
    db.close()

    try:
        mention_staff = interaction.guild.get_role(int(db.fetch('staff_role')))
        if mention_staff == None:
            raise ValueError
        mention_staff = f'||{mention_staff.mention}||\n'
    except:
        mention_staff = ''

    if buttons:
        raise NotImplementedError
    else:
        thread = await channel.create_thread(name=f'Ticket #{ticket_number}', type = nextcord.ChannelType.private_thread, 
            reason=f'Created Ticket # {ticket_number} for {interaction.user.name}.')
        if reason != None:
            reasoning = f"\nReason: *{reason}*"
        else:
            reasoning = ""
        init = await thread.send(f'**{thread.name}** opened by {interaction.user.mention}\n{mention_staff}{reasoning}\nTo close this ticket, use the `/ticket close` slash command.\n\
To add people to the ticket, simply **@mention** them.')
        await init.pin(reason = 'Initial ticket message')
    
    await interaction.send(f'*Ticket Opened in {thread.mention}*')
        

async def is_ticket(thread: nextcord.Thread or nextcord.Channel, debug: bool = False):
    """ Check if a Thread is a ticket
    Returns: bool """
    if debug:
        def negative(reason):
            return False, reason
        def affirmative():
            return True, None
    else:
        def negative(reason):
            return False
        def affirmative():
            return True
    
    if thread.type != nextcord.ChannelType.private_thread:
        return negative('Not a private thread')
    
    db = Database(thread.guild, reason='Ticketing, checking if thread is ticket')

    if not db.fetch('ticket_channel').isdigit():
        return negative('`ticket_channel` is not set')
    elif int(db.fetch('ticket_channel')) != thread.parent_id:
        return negative('Not a child of `ticket_channel`.')

    number = thread.name.replace("Ticket #", "")
    if number.isdigit(): # Check if name is 'Thread #0' etc.
        if not db.fetch('ticket_int').isdigit():
            return negative('`ticket_int` is not set! (no tickets have been made)')
        if not int(number) <= int(db.fetch('ticket_int')):
            return negative('Thread number in name is higher than expected')
    else:
        return negative(f'Not named as a thread should be')
    
    return affirmative()

async def get_ticket_creator(thread: nextcord.Thread):
    """ Get the User who created this ticket
    This is done by iterating though history near thread creation time (to get the bot's initial message),
     and returning the first user mentioned.
    NOTE: This does NOT check if this thread is a ticket. """
    
    history = await thread.history(limit=10, around=thread.created_at).flatten()
    for message in history:
        first = message # After
    
    return message.mentions[0]
    
async def close(interaction: nextcord.Interaction):
    """ Close a Ticket """
    db = Database(interaction.guild, reason='Ticketing, close ticket')

    if not await is_ticket(interaction.channel):
        await interaction.send(f'Run this command in the ticket you wish to close.', ephemeral=True)
        return
    thread = interaction.channel # interaction is discarded upon response
    user = interaction.user
    await interaction.response.defer()  

    creator = await get_ticket_creator(thread)
    await interaction.send(f'**🎟️ Ticket Closed.**')
    await thread.edit(name=f'{thread.name} [Closed]', archived=True, locked=True)
    await creator.send(f'{thread.name} has been closed. You can view it here: {thread.mention}.')
    await moderation.modlog(interaction.guild, '🎟️ Ticket Closed', interaction.user, creator, additional = {'Thread':thread.mention})
