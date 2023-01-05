from logging42 import logger
import nextcord
from nextcord.ext import commands
import yaml
import os

class Git(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    with open("config/config.yml", "r") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
    TESTING_GUILD_ID=cfg["discord"]["testing_guild"]

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        logger.info('Loaded cog git.py')

    bot = commands.Bot()

    # Commands
    @nextcord.slash_command(description="Pull from git", guild_ids=[TESTING_GUILD_ID])
    async def git_pull(self, interaction: nextcord.Interaction):
        await interaction.response.send_message(f'{os.system("cd /home/tiramisu/Tiramisu; git pull")}')
        logger.info(f"Pulled from git.")

def setup(bot):
    bot.add_cog(Git(bot))
    logger.debug('Setup cog "git"')