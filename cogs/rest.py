# 
# Tiramisu Discord Bot
# --------------------
# REST API
# 
from logging42 import logger
import nextcord
from nextcord.ext import commands
import yaml
import json
import secrets

import asyncio
import concurrent.futures

from libs.database import Database

from libs import moderation

import logging

from aiohttp import web

class API(commands.Cog):
    def __init__(self, bot):
        """ REST API Processor for modlog submissions
        It processes requests that the REST API places in the queue.yml file, and generates secrets. """
        self.bot = bot    
        with open("config/config.yml", "r") as ymlfile:
            self.cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

        try:
            with open(self.cfg['api']['secret'], 'r') as f:
                secret = f.readlines()[0].strip(' \n')
        except FileNotFoundError:
            secret = ''
        if secret == '':
            with open(self.cfg['api']['secret'], 'w') as f:
                secret = secrets.token_urlsafe(32)
                f.write(secret)
        self.secret = secret

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        logger.info('Loaded cog rest.py (Beta)')
        if not self.running:
            self.server()

    # Commands
    @nextcord.slash_command(description="Manage REST API")
    async def api(self, interaction: nextcord.Interaction):
        pass

    @api.subcommand(description='Get secrets for REST API')
    async def secret(self, interaction: nextcord.Interaction):
        db = Database(interaction.guild, reason='Slash command, /api secret')
        if interaction.user.id in db.fetch('admins'):
            guild_secret = db.fetch('api_secret')
            if guild_secret == 'none':
                guild_secret = secrets.token_urlsafe(16)
                db.set('api_secret', guild_secret)
                db.close()
            msg = f'### Secrets\n*Do not share these!*\nInstance Secret: `{self.secret}`\nGuild Secret: `{guild_secret}`'
            await interaction.send(msg, ephemeral=True)
    
        else:
            await interaction.send(self.cfg['messages']['noperm'])
    

def setup(bot):
    with open("config/config.yml", "r") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
    if cfg['api']['enabled']:
        bot.add_cog(API(bot))
        logger.debug('Setup cog "rest"')
        logger.warning('Enabling REST API Processor: This is a beta feature! Expect bugs!')