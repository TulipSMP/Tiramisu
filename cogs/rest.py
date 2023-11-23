# 
# Tiramisu Discord Bot
# --------------------
# REST API
# 
from logging42 import logger
import nextcord
from nextcord.ext import commands
import yaml
import secrets
from libs.database import Database

from libs import moderation


class API(commands.Cog):
    def __init__(self, bot):
        """ REST API for modlog submissions """
        try:
            from flask import Flask, request, jsonify
        except:
            logger.error('Failed to enable REST API! flask is not installed.')
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

        self.app = Flask(__name__)

        @self.app.route('/modlog/<str:guild_id>', methods=['POST', 'PUT'])
        def modlog(guild_id):
            # Load and Parse Data
            data = json.loads(request.data)
            try:
                instance_secret = data["instance_secret"]
                guild_secret = data["guild_secret"]
                action = data["action"]
                user = data["user"]
                platform = data["platform"]
                reason = data["reason"]
                author = data["author"]
            except KeyError:
                return 'Missing Required Arguments', 400

            # Authenticate
            if instance_secret != self.secret:
                return 'Invalid Instance Secret', 401

            # Parse optional data
            if 'duration' in data:
                duration = data['duration']
            else:
                duration = None
            if 'notes' in data:
                notes = data["notes"]
            else:
                notes = None

            # Fetch Guild
            try:
                guild = await self.bot.fetch_guild(int(guild_id))
                if guild == None:
                    raise KeyError
            except KeyError:
                return 'Guild Not Found', 404
            
            # Authenticate against Guild
            db = Database(guild, reason='REST API Authentication')
            if guild_secret != db.fetch('api_secret'):
                return 'Invalid Guild Secret', 401
            
            # Create Modlog Entry
            extra = {}
            extra["Platform"] = platform
            if duration != None:
                extra["Duration"] = duration
            if notes != None:
                extra["Notes"] = notes
            extra["INFO"] = 'Published via REST API.'
            response = await moderation.modlog(
                guild,
                action,
                author,
                user,
                reason = reason,
                additional = extra
            )

            # Respond
            return str(response), 200

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        logger.info('Loaded cog rest.py (Beta)')

    # Commands
    @nextcord.slash_command(description="Manage REST API")
    async def api(self, interaction: nextcord.Interaction):
        pass

    @api.subcommand(description='Get secrets for REST API')
    async def secret(self, interaction: nextcord.Interacion):
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
    
    # API Server
    async def main(self):
        self.app.run(debug=False)


def setup(bot):
    with open("config/config.yml", "r") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
    if cfg['api']['enabled']:
        bot.add_cog(API(bot))
        logger.debug('Setup cog "rest"')
        logger.warn('Enabling REST API: This is a beta feature! Expect bugs!')