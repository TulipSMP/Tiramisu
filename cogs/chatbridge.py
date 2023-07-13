# 
# Tiramisu Discord Bot
# --------------------
# Chat Bridge
# 
from logging42 import logger

import nextcord
from nextcord.ext import commands

import yaml
import websockets
import json

from libs.database import Database
from libs import utility, moderation

class Bridge(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
        with open("config/config.yml", "r") as ymlfile:
            self.cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        logger.info('Loaded cog chatbridge.py')

    @commands.Cog.listener()
    async def on_message(self):
        pass # Send to other side of websocket

    @nextcord.slash_command(description='Manage Bridge')
    async def bridge(self, interaction):
        pass

    @bridge.subcommand(description='Get Bridge UUID')

def setup(bot):
    bot.add_cog(Bridge(bot))
    logger.debug('Setup cog "chatbridge"')