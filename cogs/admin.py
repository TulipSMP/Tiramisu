from logging42 import logger
import nextcord
from nextcord.ext import commands
import yaml
import mysql.connector

class Catboy(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    with open("config/config.yml", "r") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
    TESTING_GUILD_ID=cfg["discord"]["testing_guild"]

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        logger.info('Loaded cog admin.py')

    # Commands
    @nextcord.slash_command(guild_ids=[TESTING_GUILD_ID])
    async def admin(self, interaction: nextcord.Interaction):
        pass
        # This command is to set up the following as subcommands
    
    @nextcord.slash_command(description="[Admin] Add and administrator", guild_ids=[TESTING_GUILD_ID])
    async def add(self, interaction: nextcord.Interaction, user: nextcord.Interaction.user):
        if interaction.user.id == interaction.user.owner_id:
            await interaction.send(f"Adding {user.mention} as an admin.", ephemeral=True)
            await interaction.send("Error: not set up.")
            logger.debug(f'{interaction.user.name} added {user.name}')
        else:
            await interaction.send(cfg["messages"]["noperm"], ephemeral=True)

def setup(bot):
    bot.add_cog(Admin(bot))
    logger.debug('Setup cog "admin"')