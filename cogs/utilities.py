from logging42 import logger
import nextcord
from nextcord.ext import commands
import yaml
from libs.database import Database

class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open("config/config.yml", "r") as ymlfile:
            self.cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
    
    with open("config/config.yml", "r") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
    TESTING_GUILD_ID = cfg['discord']['testing_guild']

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        logger.info('Loaded cog utilities.py')

    # Commands
    @nextcord.slash_command(description="Get the game server IP", guild_ids=[TESTING_GUILD_ID])
    async def ip(self, interaction: nextcord.Interaction):
        db = Database(interaction.guild, reason='Slash command `/ip`')
        ip = db.fetch('ip_address')
        text = db.fetch('ip_text')
        game = db.fetch('ip_game')
        warn = ''
        if ip == 'none':
            warn += '\nAsk the admins to change the setting `ip_address`'
        if text == 'none':
            text = ''
            warn += '\nAsk the admins to change the setting `ip_text` to show a description.'
        if game == 'none':
            warn += '\nAsk the admins to change the setting `ip_game` to which game their server is for.'
        await interaction.send(f'**{game.title()} Server IP:** `{ip}`\n{text}{warn}')

def setup(bot):
    bot.add_cog(Utilities(bot))
    logger.debug('Setup cog "utilities"')