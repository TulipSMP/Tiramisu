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

    # Commands
    @commands.command(description="Hello!", guild_ids=[TESTING_GUILD_ID])
    async def hello(self, interaction: nextcord.Interaction):
        await interaction.response.send_message(f"Hello World! I'm {bot.user}!")
        await print(f"Said hello to {interaction.user.name}.")

    @nextcord.slash_command(guild_ids=[TESTING_GUILD_ID])
    async def slashcog(self, interaction: nextcord.Interaction):
        #  This is a slash command in a cog
        await interaction.response.send_message("Hello I am a slash command in a cog!")

def setup(bot):
    bot.add_cog(Hello(bot))