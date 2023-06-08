# 
# Tiramisu Discord Bot
# --------------------
# Ticketing System
# 
import nextcord
import random

from libs import utility, modals, buttons, moderation
from libs.database import Database

async def create(interaction: nextcord.Interaction, reason: str = None, buttons: bool = False):
    """ Create a Ticket """
    if reason == None:
        await interaction.response.send_modal(modals.InputModal('Create a Ticket', 'Topic of ticket', create)) # Call create again with reason
        return
    elif interaction.channel.type != nextcord.ChannelType.text:
        await interaction.response.send_message('I cannot create tickets here!')
        return

    db = Database(interaction.guild, reason='Ticketing, increasing ticket number')
    ticket_number = db.fetch('ticket_int')
    if ticket_number == 'none':
        ticket_number = 0
    elif ticket_number.isdigit():
        ticket_number = int(ticket_number)
    else:
        ticket_number = 0
    ticket_number += 1
    db.set('ticket_int', str(ticket_number))

    if buttons:
        raise NotImplementedError
    else:
        thread = await interaction.channel.create_thread(name=f'Ticket #{ticket_number}', type = nextcord.ChannelType.private_thread, 
            reason=f'Created Ticket # {ticket_number} for {interaction.user.name}.')

async def close(interaction: nextcord.Interaction, thread: nextcord.Thread, creator: nextcord.Member):
    """ Close a Ticket """
    user = interaction.user
    await interaction.send('Closing ticket...', ephemeral=True)

    await thread.edit(name=f'{thread.name} [Closed]', archived=True, locked=True)

    await creator.send_message(f'{thread.name} has been closed. You can view it here: {thread.mention}.')

    await moderation.modlog(interaction.guild, '🎟️ Ticket Closed', user, creator, additional = {'Thread':thread.mention})

