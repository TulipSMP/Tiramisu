# 
# Tiramisu Discord Bot
# --------------------
# Listener for libs.logging
# 
from logging42 import logger
import nextcord
from nextcord.ext import commands
import yaml
from libs import logging


class Logging(commands.Cog):
    def __init__(self, bot):
        """ Boilerplate Cog. Also funny fizzdev catboy hahaha """
        self.bot = bot    
        with open("config/config.yml", "r") as ymlfile:
            self.cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)


    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        logger.info('Loaded cog logging.py')

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        await logging.log(logging.DeletedMessage(message))
    
    @commands.Cog.listener()
    async def on_message_edit(self, old, new):
        await logging.log(logging.EditedMessage(old, new))

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        await logging.log(logging.ChangeVoice(member, before, after))
        

def setup(bot):
    bot.add_cog(Logging(bot))
    logger.debug('Setup cog "logging"')