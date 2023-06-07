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

        self.broadcast = nextcord.ui.Select(label='Publicly send Warn?',min_values=1, max_values=1)
        self.broadcast.add_option('True')
        self.broadcast.add_option('False')
        self.add_item(self.broadcast)

    async def callback(self, interaction: nextcord.Interaction):
        db = Database(interaction.guild, reason=f'Check for permission, libs.ui.modals.WarnModal')
        if interaction.user.id in db.fetch('admins') or utility.is_mod(interaction.user, db):
            if 'True' in self.broadcast.values:
                broadcast = True
            else:
                broadcast = False
            await moderation.warn(interaction, self.user, self.reason.value, broadcast=broadcast)
        else:
            await interaction.send(self.cfg['messages']['noperm'], ephemeral=True)