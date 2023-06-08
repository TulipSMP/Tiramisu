# 
# Tiramisu Discord Bot
# --------------------
# Ticketing System
# 
import nextcord
import random

from libs import utility, modals, buttons
from libs.database import Database

async def create(interaction: nextcord.Interaction, reason: str = None):
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
    await interaction.channel.create_thread(name=f'Ticket #{ticket_number}')
    db.set('ticket_int', str(ticket_number))
