from logging42 import logger
import nextcord
from nextcord.ext import commands
import yaml
from typing import Optional

from libs.database import Database


class Help(commands.Cog):
    def __init__(self, bot):
        """ Boilerplate Cog. Also funny fizzdev catboy hahaha """
        self.bot = bot    
        with open("config/config.yml", "r") as ymlfile:
            self.cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

        with open("config/help.yml", "r") as ymlfile:
            self.help = yaml.load(ymlfile, Loader=yaml.FullLoader)


    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        logger.info('Loaded cog help.py')

    # Must be opened here for function definition
    with open("config/help.yml", "r") as ymlfile:
        HELP = yaml.load(ymlfile, Loader=yaml.FullLoader)
    help_topics = dict()
    for topic in HELP:
        help_topics[HELP[topic]['name']] = topic
    HELP_TOPICS = help_topics

    # Commands
    @nextcord.slash_command(description="Try me!")
    async def help(self, interaction: nextcord.Interaction, topic: Optional[str] = nextcord.SlashOption(description='What do you need help with?',
            choices=HELP_TOPICS, required=False, default='main')):
        try:
            message = self.help[topic]['content'].replace('[[BOT]]', self.bot.user.name)
        except KeyError:
            await interaction.send('*The specified help topic was not found.*')
            return
        
        await interaction.send(message)

def setup(bot):
    bot.add_cog(Help(bot))
    logger.debug('Setup cog "help"')