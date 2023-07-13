# 
# Tiramisu Discord Bot
# --------------------
# Buttons
# 
import nextcord
from nextcord.ext import menus, commands
from logging42 import logger

from libs import ticketing, applications

class HelloButton(menus.ButtonMenu):
    def __init__(self):
        """ Says Hello! """
        super().__init__(disable_buttons_after=True)


    async def send_initial_message(self, interaction, channel):
        logger.warning(f'{type(interaction)} / {interaction}')
        #await interaction.send('Working...')
        return await channel.send(f'Press the button below!')

    @nextcord.ui.button(label='Try Me!', emoji="❓", custom_id='tiramisu:hello', style=nextcord.ButtonStyle.blurple)
    async def on_hello(self, button, interaction: nextcord.Interaction):
        await interaction.send(f'Hello {interaction.user.display_name}!')

class TicketsButton(nextcord.ui.View):
    def __init__(self):
        """ Button to Create a Ticket"""
        super().__init__(timeout=None)

    @nextcord.ui.button(label='Ticket',emoji="🎟️", custom_id='tiramisu:create_ticket', style=nextcord.ButtonStyle.success)
    async def on_create(self, button, interaction: nextcord.Interaction):
        await ticketing.create(interaction)

class TicketCloseButton(nextcord.ui.View):
    def __init__(self):
        """ Button for Closing a Ticket """
        super().__init__(timeout=None)

    @nextcord.ui.button(label='Close', emoji="🗑️", custom_id=f'tiramisu:close_ticket', style=nextcord.ButtonStyle.red)
    async def on_close(self, button, interaction: nextcord.Interaction):
        await ticketing.close(interaction)
        self.clear_items()

class PersistentTextButton(nextcord.ui.View):
    def __init__(self):
        """ Testing Persistent Buttons: https://github.com/nextcord/nextcord/blob/master/examples/views/persistent.py """
        super().__init__(timeout=None)
    
    @nextcord.ui.button(label='Test', style=nextcord.ButtonStyle.gray, custom_id='tiramisu:libs-buttons-persistent-text-button')
    async def test(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_message("Yup! it works!")

class ApplicationButton(nextcord.ui.View):
    def __init__(self):
        """ Button to Create a Mod Application """
        super().__init__(timeout=None)

    @nextcord.ui.button(label='Apply',emoji="⛑️", custom_id='tiramisu:create_application', style=nextcord.ButtonStyle.success)
    async def on_create(self, button, interaction: nextcord.Interaction):
        await applications.answer_and_create(interaction)

class ApplicationActions(nextcord.ui.View):
    def __init__(self):
        """ Button for Closing an Application """
        super().__init__(timeout=None)

    @nextcord.ui.button(label='Accept', emoji="✅", custom_id=f'tiramisu:accept_application', style=nextcord.ButtonStyle.success)
    async def on_close(self, button, interaction: nextcord.Interaction):
        await applications.accept(interaction)
        self.clear_items()

    @nextcord.ui.button(label='Close', emoji="🗑️", custom_id=f'tiramisu:close_application', style=nextcord.ButtonStyle.red)
    async def on_close(self, button, interaction: nextcord.Interaction):
        await applications.close(interaction)
        self.clear_items()