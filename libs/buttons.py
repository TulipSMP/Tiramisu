# 
# Tiramisu Discord Bot
# --------------------
# Buttons
# 
import nextcord
from nextcord.ext import menus

from libs import ticketing

class TicketsButton(menus.ButtonMenu):
    def __init__(self):
        """ Button for Tickets System """
        super().__init__()

    async def send_initial_message(self, interaction, channel):
        """ Send message containing buttons """
        return await channel.send(f'## Create a Ticket\nClick the button below to create a ticket so that others can chat with you.')

    @nextcord.ui.button(emoji="✅", custom_id='tiramisu:create_ticket', style=nextcord.ui.ButtonStyle.success)
    async def on_create(self, button, interaction: nextcord.Interaction):
        await ticketing.create(interaction)
