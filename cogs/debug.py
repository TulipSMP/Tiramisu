from logging42 import logger
import nextcord
from nextcord.ext import commands
import yaml
from libs.database import Database

class Debug(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    with open("config/config.yml", "r") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
    TESTING_GUILD_ID=cfg["discord"]["testing_guild"]

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        logger.info('Loaded cog hello.py')

    bot = commands.Bot()

    # Commands
    @nextcord.slash_command(description='Commands for Debugging', guild_ids=[TESTING_GUILD_ID])
    async def debug(self, interaction: nextcord.Interaction):
        pass

    @debug.subcommand(description="Print DB")
    async def db(self, interaction: nextcord.Interaction, settings=False):
        db = Database(interaction.guild, reason='Fetch for debugging')
        if settings:
            t_type = 'settings'
        else:
            t_type = 'admin'
        table = db.raw(f'select * from {t_type}_{db.guild.id};')
        if table == False:
            table = 'Failed to fetch from guild! OperationalError!'
        else:
            await interaction.response.send_message(f"Found these values in table `{t_type}_{db.guild.id}`: ```\n{table} ```")
        logger.debug(f"Said hello to {interaction.user.name}.")

def setup(bot):
    bot.add_cog(Debug(bot))
    logger.debug('Setup cog "debug"')