import nextcord
from nextcord.ext import commands


class Catboy(commands.Cog):
    def __init__(self, bot):
        self.client = bot
    
    TESTING_GUILD_ID=1035313572638638110

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print('Cog catboy.py loaded!')

    # Commands
    @commands.command(description="Try me!", guild_ids=[TESTING_GUILD_ID])
    async def fizz(interaction: nextcord.Interaction):
        await interaction.send(f"Yes, fizz is indeed a catboy. I am a discord bot so I am always right.")
        print(f"Reminded {interaction.user.name} that fizzdev is indeed a catboy.")

def setup(bot):
    bot.add_cog(Catboy(bot))