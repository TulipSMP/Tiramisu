# 
# Tiramisu Discord Bot
# --------------------
# Right-Click Mod Actions
# 
from logging42 import logger

import yaml
import nextcord
from nextcord.ext import commands

from libs.database import Database
from libs import moderation, utility

class ModRightclick(commands.Cog):
    def __init__(self, bot):
        """ Perform moderation actions by right-clicking users """
        self.bot = bot    
        with open("config/config.yml", "r") as ymlfile:
            self.cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)


    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        logger.info('Loaded cog mod_rightclick.py')

    # Commands
    @nextcord.message_command(name='Warn for Message')
    async def warn(self, interaction: nextcord.Interaction, message: nextcord.Message):
        """ Warn a User """
        db = Database(interaction.guild, reason=f'Check for permission, `/warn`')
        if interaction.user.id in db.fetch('admins') or utility.is_mod(interaction.user, db):
            if len(message.content) <= 40:
                msg_summary = message.content
            else:
                msg_summary = f'{message.content[0:35]}...'

            await moderation.warn(interaction, self.bot.user, message.author, f'Message: {message.jump_url}', dm=True, broadcast=True)
        else:
            await interaction.send(self.cfg['messages']['noperm'], ephemeral=True)

def setup(bot):
    bot.add_cog(ModRightclick(bot))
    logger.debug('Setup cog "mod_rightclick"')