# 
# Tiramisu Discord Bot
# --------------------
# Ticketing Interactions
# 
from logging42 import logger

import nextcord
from nextcord.ext import commands

import yaml
from typing import Optional

from libs.database import Database
from libs import utility, moderation, ticketing, buttons

class Ticketing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.button_added = False
    
        with open("config/config.yml", "r") as ymlfile:
            self.cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        logger.info('Loaded cog tickets.py')
        if not self.button_added:
            self.bot.add_view(buttons.TicketsButton())
            self.bot.add_view(buttons.TicketCloseButton())
            self.button_added = True

    # Commands
    @nextcord.slash_command(description="Manage Tickets")
    async def ticket(self, interaction: nextcord.Interaction):
        pass # To setup subcommands

    @ticket.subcommand(description="Create a Ticket")
    async def create(self, interaction: nextcord.Interaction):
        await ticketing.create(interaction)
    
    @ticket.subcommand(description='Close this Ticket')
    async def close(self, interaction: nextcord.Interaction):
        await ticketing.close(interaction)


    @ticket.subcommand(description='Create a button for creating tickets')
    async def button(self, interaction: nextcord.Interaction,
        info: Optional[str] = nextcord.SlashOption(description='Additional text for the resulting message', required=False, default='Click the button below to create a ticket.')):
        db = Database(interaction.guild, reason='Ticket Button Create, check perms')
        if utility.is_mod(interaction.user, db) or interaction.user.id in db.fetch('admins'):
            await interaction.channel.send(f'## Create a Ticket\n{info}', view=buttons.TicketsButton())
            await interaction.send('Created Button!', ephemeral=True)
        else:
            await interaction.send(self.cfg['messages']['noperm'], ephemeral=True)


def setup(bot):
    bot.add_cog(Ticketing(bot))
    logger.debug('Setup cog "tickets"')