# 
# Tiramisu Discord Bot
# --------------------
# Reports System
# 
from logging42 import logger

import nextcord

from libs.database import Database
from libs import modals, buttons

async def bug(interaction: nextcord.Interaction):
    """ Handle a bug report """
    db = Database(interaction.guild, reason='Slash command `/report user`')
    try:
        bugreports_channel =  interaction.guild.get_channel(int(db.fetch('bugreports_channel')))
        if bugreports_channel == None:
            raise ValueError
        else:
            default = [
                "Where does this bug occur?",
                "What happens when this bug occurs?",
                "What should happen instead?",
                "How do you make this bug happen?",
                "Additional Info:"
            ]
            questions = db.fetch('bugreports_questions')
            if questions == 'none':
                questions = default
            else:
                questions = questions.split(';')
            await interaction.response.send_modal(modals.BugReportModal(bugreports_channel, questions))
    except ValueError:
        await interaction.send('Bug reports are not set up on this server.\nAsk an administrator to set the `bugreports_channel` setting to a proper channel.', ephemeral=True)

async def player(interaction: nextcord.Interaction):
    """ Handle a Player Report """
    await interaction.response.defer()
    db = Database(interaction.guild, reason='libs.reports:player check if modlog is setup before report')
    try:
        channel = interaction.guild.get_channel(int(db.fetch('modlog_channel')))
        if channel == None:
            raise ValueError
    except ValueError:
        await interaction.send('The Modlog is not set up, so there is nowhere for me to send reports!\nAsk an administrator to set the `modlog_channel` setting to an appropriate channel.', ephemeral=True)
        return
    
    await interaction.response.send_modal(modals.PlayerReportModal())