# 
# Tiramisu Discord Bot
# --------------------
# Suggestions Library
# 
from logging42 import logger

import yaml
import nextcord
from typing import Optional

from libs.database import Database
from libs import utility, buttons, modals

async def suggest(interaction: nextcord.Interaction, suggestion: Optional[str]):
    """ Create a Suggestion and handle the interaction """
    db = Database(interaction.guild, reason='Suggestions, suggest')
    try:
        channel = interaction.guild.get_channel(int(db.fetch('suggestions_channel')))
        if channel == None:
            raise ValueError
    except ValueError:
        await interaction.send(f'*Suggestions are not set up. Ask an administrator to set the `suggestions_channel` setting to an appropriate channel.*', ephemeral=True)
        return

    if suggestion == None:
        await interaction.response.send_modal(modals.InputModal('Suggestion', 'Describe your Suggestion:', suggest))
    else:
        await interaction.response.defer(ephemeral=True)

        message = await channel.send(f'### Suggestion by {interaction.user.mention} \n>>> {suggestion}', view=buttons.SuggestionActions())

        await interaction.send(f'Suggestion Sent! *See {message.jump_url}*', ephemeral=True)

async def upvote(interaction: nextcord.Interaction, button: nextcord.ui.Button):
    """ Upvote a Suggestion """
    try:
        button.label = int(button.label) + 1
    except:
        button.label = 1
    
    await interaction.response.edit_message(view=button)
    await interaction.send(f'Upvoted!', ephemeral=True)

async def downvote(interaction: nextcord.Interaction, button: nextcord.ui.Button):
    """ Downvote a Suggestion """

async def accept(interaction: nextcord.Interaction, button: nextcord.ui.Button, view: nextcord.ui.View):
    """ Accept a Suggestion """

async def deny(interaction: nextcord.Interaction, button: nextcord.ui.Button, view: nextcord.ui.View):
    """ Deny a Suggestion """
