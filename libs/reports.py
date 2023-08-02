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
    db = Database(interaction.guild, reason='Slash command `/report user`')
    try:
        bugreports_channel =  interaction.guild.get_channel(int(db.fetch('bugreports_channel')))
        if bugreports_channel == None:
            raise ValueError
        else:
            #place: Optional[str] = nextcord.SlashOption(description='Where does this bug occur?', required=True),
            #behavior: Optional[str] = nextcord.SlashOption(description='What happens when this bug occurs?', required=True),
            #expected: Optional[str] = nextcord.SlashOption(description='What should happen instead of this bug?', required=True),
            #reproduce: Optional[str] = nextcord.SlashOption(description='What do you have to do for this bug to happen?', required=True),
            #extra: Optional[str] = nextcord.SlashOption(description='Other info that might be helpful to us in fixing this bug', required=False, default=None)):
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
            await interaction.channel.send_modal(modals.BugReportModal(bugreports_channel, questions))
    except ValueError:
        await interaction.send('Bug reports are not set up on this server.\nAsk an administrator to set the `bugreports_channel` setting to a proper channel.', ephemeral=True)