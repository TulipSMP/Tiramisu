# 
# Tiramisu Discord Bot
# --------------------
# Modals
#
import nextcord
from logging42 import logger

from libs.database import Database
from libs import moderation, utility

class WarnModal(nextcord.ui.Modal):
    def __init__(self, user: nextcord.Member):
        """ Modal for Warning User via Context Menu """
        super().__init__(f'Warn {user.display_name}', timeout=600)
        self.user = user

        # Components
        self.reason = nextcord.ui.TextInput(
            label = 'Reason for Warn',
            min_length = 2,
            max_length = 25
        )
        self.add_item(self.reason)

    async def callback(self, interaction: nextcord.Interaction):
        db = Database(interaction.guild, reason=f'Check for permission, libs.ui.modals.WarnModal')
        if interaction.user.id in db.fetch('admins') or utility.is_mod(interaction.user, db):
            await moderation.warn(interaction, self.user, self.reason.value)
        else:
            await interaction.send(self.cfg['messages']['noperm'], ephemeral=True)

class BanModal(nextcord.ui.Modal):
    def __init__(self, user: nextcord.Member):
        """ Modal for Banning User via Context Menu """
        super().__init__(f'Ban {user.display_name}', timeout=600)
        self.user = user

        # Components
        self.reason = nextcord.ui.TextInput(
            label = 'Reason for Ban',
            min_length = 2,
            max_length = 25
        )
        self.add_item(self.reason)

    async def callback(self, interaction: nextcord.Interaction):
        db = Database(interaction.guild, reason=f'Check for permission, libs.ui.modals.BanModal')
        if interaction.user.id in db.fetch('admins') or utility.is_mod(interaction.user, db):
            await moderation.ban(interaction, self.user, self.reason.value)
        else:
            await interaction.send(self.cfg['messages']['noperm'], ephemeral=True)

class KickModal(nextcord.ui.Modal):
    def __init__(self, user: nextcord.Member):
        """ Modal for Kicking User via Context Menu """
        super().__init__(f'Kick {user.display_name}', timeout=600)
        self.user = user

        # Components
        self.reason = nextcord.ui.TextInput(
            label = 'Reason for Kick',
            min_length = 2,
            max_length = 25
        )
        self.add_item(self.reason)

    async def callback(self, interaction: nextcord.Interaction):
        db = Database(interaction.guild, reason=f'Check for permission, libs.ui.modals.KickModal')
        if interaction.user.id in db.fetch('admins') or utility.is_mod(interaction.user, db):
            await moderation.kick(interaction, self.user, self.reason.value)
        else:
            await interaction.send(self.cfg['messages']['noperm'], ephemeral=True)

class InputModal(nextcord.ui.Modal):
    def __init__(self, title, label, callback, timeout=300, min_length = 2, max_length = 15, *args, **kwargs):
        """ Modal for Entering a reason and creating a ticket 
        * `title`: Title for the modal
        * `label`: Label for the input box
        * `callback`: function to call for returning input. Is sent two parameters:
          - `nextcord.Interaction`: the interaction
          - `str`: The input from the user"""
        super().__init__(f'{title}', timeout=timeout)
        self.ext_callback = callback

        # Components
        self.input = nextcord.ui.TextInput(
            label = label,
            min_length = min_length,
            max_length = max_length,
            *args, **kwargs
        )
        self.add_item(self.input)

    async def callback(self, interaction: nextcord.Interaction):
        self.ext_callback(interaction, self.input.value)
