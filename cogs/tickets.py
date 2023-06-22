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
from libs import utility, moderation, ticketing

class Ticketing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        logger.info('Loaded cog tickets.py')

    # Commands
    @nextcord.slash_command(description="Manage Tickets")
    async def ticket(self, interaction: nextcord.Interaction):
        pass # To setup subcommands

    @ticket.subcommand(description="Create a Ticket")
    async def create(self, interaction: nextcord.Interaction):
        await ticketing.create(interaction, buttons=False, require_reason=False)
    
    @ticket.subcommand(description='Close this Ticket')
    async def close(self, interaction: nextcord.Interaction):
        await ticketing.close(interaction)


def setup(bot):
    bot.add_cog(Ticketing(bot))
    logger.debug('Setup cog "tickets"')