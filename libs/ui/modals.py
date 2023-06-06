# 
# Tiramisu Discord Bot
# --------------------
# Modals
#
import nextcord

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