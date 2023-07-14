# 
# Tiramisu Discord Bot
# --------------------
# Suggestions
# 
from logging42 import logger

import nextcord
from nextcord.ext import commands

import yaml

from libs.database import Database
from libs import utility, moderation, buttons

class Suggestions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.views_added = False
    
        with open("config/config.yml", "r") as ymlfile:
            self.cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
        TESTING_GUILD_ID=cfg["discord"]["testing_guild"]

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        logger.info('Loaded cog suggestions.py')

        if not self.views_added:
            self.bot.add_view(buttons.SuggestionButton)
            self.bot.add_view(buttons.SuggestionActions)
            self.views_added = True

    # Commands
    @nextcord.slash_command()
    async def suggestions(self, interaction: nextcord.Interaction):
        pass # For subcommands

    @suggestions.subcommand(description='Create a Suggestions button')
    async def button(self, interaction: nextcord.Interaction,
        info: Optional[str] = nextcord.SlashOption(description='Additional text for the resulting message', required=False, default='Click the button below to make a Suggestion.')):
        db = Database(interaction.guild, reason='Suggestion Button Create, check perms')
        if utility.is_mod(interaction.user, db) or interaction.user.id in db.fetch('admins'):
            await interaction.channel.send(f'## Create a Suggestion\n{info}', view=buttons.SuggestionButton())
            await interaction.send('Created Button!', ephemeral=True)
        else:
            await interaction.send(self.cfg['messages']['noperm'], ephemeral=True)
    

def setup(bot):
    bot.add_cog(Suggestions(bot))
    logger.debug('Setup cog "suggestions"')