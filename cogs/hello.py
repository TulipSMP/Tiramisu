from logging42 import logger
import nextcord
from nextcord.ext import commands


class Hello(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    TESTING_GUILD_ID=1035313572638638110

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print('Cog hello.py loaded!')
        logger.info('Loaded cog hello.py')

    # Commands
    @nextcord.slash_command(description="Hello!", guild_ids=[TESTING_GUILD_ID])
    async def hello(self, interaction: nextcord.Interaction):
        await interaction.response.send_message(f"Hello {interaction.user.display_name}! I'm {bot.display_name}!")
        logger.debug(f"Said hello to {interaction.user.name}.")

def setup(bot):
    bot.add_cog(Hello(bot))
    logger.debug('Setup cog "hello"')