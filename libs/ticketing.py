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
        init = thread.send(f'**{thread.name}** opened by {interaction.user.mention}\n{mention_staff}{reasoning}\nTo close this ticket, use the `/ticket close` slash command.')
        await init.pin(reason = 'Initial ticket message')
        

async def close(interaction: nextcord.Interaction):
    """ Close a Ticket """
    db = Database(interaction.guild, reason='Ticketing, close ticket')
    user = interaction.user
    if interaction.channel.type != nextcord.ChannelType.private_thread or interaction.channel:
        await interaction.send(f'Run this command in the ticket you wish to close.', ephemeral=True)
        return

    await thread.edit(name=f'{thread.name} [Closed]', archived=True, locked=True)

    await creator.send_message(f'{thread.name} has been closed. You can view it here: {thread.mention}.')

    await moderation.modlog(interaction.guild, '🎟️ Ticket Closed', user, creator, additional = {'Thread':thread.mention})

