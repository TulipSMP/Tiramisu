import random
from logging42 import logger
import nextcord
from nextcord.ext import commands

class FunCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        logger.info('Loaded cog fun_commands.py')
    
    # 8ball Command
    @nextcord.slash_command(description="Ask the magic 8ball a question!")
    async def eight_ball(self, interaction: nextcord.Interaction):
        responses = [
            "It is certain.",
            "It is decidedly so.",
            "Without a doubt.",
            "Yes - definitely.",
            "You may rely on it.",
            "As I see it, yes.",
            "Most likely.",
            "Outlook good.",
            "Yes.",
            "Signs point to yes.",
            "Reply hazy, try again.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again.",
            "Don't count on it.",
            "My reply is no.",
            "My sources say no.",
            "Outlook not so good.",
            "Very doubtful.",
        ]
        response = random.choice(responses)
        await interaction.response.send_message(response)
    
    # Dice Command
    @nextcord.slash_command(description="Roll a dice!")
    async def dice(self, interaction: nextcord.Interaction):
        result = random.randint(1, 6)
        await interaction.response.send_message(f"You rolled a {result}!")
    
    # Coinflip Command
    @nextcord.slash_command(description="Flip a coin!")
    async def coinflip(self, interaction: nextcord.Interaction):
        result = random.choice(["heads", "tails"])
        await interaction.response.send_message(f"The coin landed on {result}!")
    
def setup(bot):
    bot.add_cog(FunCommands(bot))
    logger.info('Setup cog "fun_commands"')
