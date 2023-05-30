# 
# Tiramisu Discord Bot
# --------------------
# Entertainment Commands
# 
from logging42 import logger
import random
import nextcord
from nextcord.ext import commands
from typing import Optional

class FunCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        logger.info('Loaded cog fun_commands.py')
    
    # 8ball Command
    @nextcord.slash_command(description="Ask the magic 8ball a question!")
    async def eight_ball(self, interaction: nextcord.Interaction,
    question: Optional[str] = nextcord.SlashOption(required=False, description="Ask the magic 8ball a question!", min_length=5, max_length=100)):
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
            "Very doubtful."
        ]
        if question == 'Is fizzdev a catboy?':
            # Use the positive responses for this specific question
            response = responses[random.randint(0, 10)]
        else:
            response = random.choice(responses)
        if random.randint(1, 250) == 69:
            response = "Certainly. Fizzdev is a catboy."
        await interaction.response.send_message(response + " 🎱")
    
    # Dice Command
    @nextcord.slash_command(description="Roll a dice!")
    async def dice(self, interaction: nextcord.Interaction, 
    type: Optional[int] = nextcord.SlashOption(choices = {'d4':4, 'd6':6, 'd8':8, 'd10':10, 'd12':12, 'd20':20, 'd100':100}, 
    description='Kind of dice to roll', required=False, default=6)):
        result = random.randint(1, type)
        await interaction.response.send_message(f"You rolled a {result}! 🎲")
    
    # Coinflip Command
    @nextcord.slash_command(description="Flip a coin!")
    async def coinflip(self, interaction: nextcord.Interaction):
        result = random.choice(["heads", "tails"])
        await interaction.response.send_message(f"The coin landed on {result}! 🪙")
    
def setup(bot):
    bot.add_cog(FunCommands(bot))
    logger.debug('Setup cog "fun_commands"')
