# 
# Tiramisu Discord Bot
# --------------------
# Buttons
# 
import nextcord
from nextcord.ext import menus, commands

from libs import ticketing

class HelloButton(menus.ButtonMenu):
    def __init__(self):
        """ Says Hello! """
        super().__init__(disable_buttons_after=True)


    async def send_initial_message(self, interaction, channel):
        logger.warning(type(interaction) + interaction)
        #await interaction.send('Working...')
        return await channel.send(f'Press the button below!')

    @nextcord.ui.button(label='Try Me!', emoji="❓", custom_id='tiramisu:hello', style=nextcord.ButtonStyle.blurple)
    async def on_hello(self, button, interaction: nextcord.Interaction):
        await interaction.send(f'Hello {interaction.user.display_name}!')

class TicketsButton(menus.ButtonMenu):
    def __init__(self):
        """ Button for Tickets System """
        super().__init__()

    async def send_initial_message(self, interaction, channel):
        """ Send message containing buttons """
        return await channel.send(f'## Create a Ticket\nClick the button below to create a ticket so that others can chat with you.')

    @nextcord.ui.button(label='New Ticket',emoji="✅", custom_id='tiramisu:create_ticket', style=nextcord.ButtonStyle.success)
    async def on_create(self, button, interaction: nextcord.Interaction):
        await ticketing.create(interaction)

class TicketCloseButton(menus.ButtonMenu):
    def __init__(self, thread: nextcord.Thread, user: nextcord.Member, message: str=None):
        """ Button for Closing a Ticket """
        super().__init__(disable_buttons_after=True)
        self.thread = thread
        self.user = user

        if message == None:
            self.message = f'**{thread.name}**\nPress the button below to close this ticket.'
        else:
            self.message = message

    async def send_initial_message(self, interaction, channel):
        return await channel.send(self.message)

    @nextcord.ui.button(label='Close', emoji="❌", custom_id=f'tiramisu:close_ticket', style=nextcord.ButtonStyle.red)
    async def on_close(self, button, interaction: nextcord.Interaction):
        await ticketing.close(interaction, self.thread, self.user)
