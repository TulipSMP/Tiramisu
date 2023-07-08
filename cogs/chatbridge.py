# 
# Tiramisu Discord Bot
# --------------------
# Chat Bridge System
# 
from logging42 import logger
import nextcord
import asyncio
import websockets

import yaml
import json
import uuid
import bcrypt
import math
import datetime

from libs.database import Database
from libs import utility, moderation, modals

class ChatBridge(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
        self.connections = {}
        self.ws_clients = set()

        self.internal_auth_uuid = str(uuid.uuid4())
        self.internal_auth_hashed = bcrypt.hashpw(self.internal_auth_uuid, bcrypt.gensalt(6))

        with open("config/config.yml", "r") as ymlfile:
            self.cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

    # Webhook Server Functions
    async def authenticate_websocket(uuid, guild) -> bool:
        """ Authenticates the websocket with the database
        uuid: the UUID for this connection
        guild: the id of the Guild to verify against """
        try:
            guild_obj = self.bot.get_guild(int(guild))
            if guild_obj == None:
                raise ValueError
        except ValueError:
            return False
        
        db = Database(guild_obj, reason='Chat Bridge, check uuid hash')
        hashed = db.fetch('chat_bridge_uuid_hashed')
        if hashed == 'none':
            return False
        else:
            return bcrypt.checkpw(uuid, hashed)

    async def register_connection(self, websocket, guild: str, channel: str):
        self.ws_clients.add(websocket)
        try:
            self.connections[guild][channel].add(websocket)
        except KeyError:
            try:
                self.connections[guild][channel] = set()
            except KeyError:
                self.connections[guild] = {}
                self.connections[guild][channel] = set()
            self.connections[guild][channel].add(websocket)


    async def handle_websocket(self, websocket):
        """ Handler for all incoming messages to the websocket server """
        if self.authenticate_websocket(msg['authority']['uuid'], msg['authority']['guild']):
            self.register_connection(websocket, msg['authority']['guild'], msg['authority']['channel'])
            external_authenticated = True
        else:
            external_authenticated = False
        msg_raw = await websocket.recv()
        logger.debug('Recieved message from websocket: {msg_raw}')
        malformed_json_response = """{
            "origin": "discord",
            "author": null,
            "message": null,
            "meta": {
                "response": 400,
                "message": "Malformed JSON"
            }
        }
        """
        bad_auth_response = """{
            "origin": "discord",
            "author": null,
            "message": null,
            "meta": {
                "response": 401,
                "message": "Authentication Failed"
            }
        }
        """

        try:
            msg = json.loads(msg_raw)
            origin = msg['origin']
        except KeyError:
            await websocket.send(malformed_json_response)
        
        # Authentication
        if origin == 'internal':
            if bcrypt.checkpw(msg['authority']['uuid'], self.internal_auth_hashed):
                try:
                    response = {
                        "origin": "discord",
                        "author": {
                            "name": msg['author']['name'],
                            "username": msg['author']['username'],
                            "id": msg['author']['id'],
                            "profile": msg['author']['profile'],
                        },
                        "message": {
                            "content": msg['message']['content'],
                            "attachments": msg['message']['attachments'],
                            "timestamp": msg['message']['timestamp'],
                        },
                        "meta": {
                            "response": 200,
                            "message": "Ok",
                        }
                    }
                    await websocket.broadcast(self.connections[ msg['authority']['guild'] ][ msg['authority']['channel'] ], json.dumps(response))
                except KeyError:
                    await websocket.send(malformed_json_response)
            else:
                await websocket.send(bad_auth_response)
        elif origin == 'external':
            if self.authenticate_websocket(msg['authority']['uuid'], msg['authority']['guild']):
                self.register_connection(websocket, msg['authority']['guild'], msg['authority']['channel'])
                # Send message to appropriate webhook
                logger.debug('Recieved external message over chat bridge')
            else:
                await websocket.send(bad_auth_response)
        elif origin == 'discord':
            pass
        else:
            response = """{
                "origin": "discord",
                "author": null,
                "message": null,
                "meta": {
                    "response": 400,
                    "message": "Unknown origin Field"
                }
            }
            """

    async def run_server_forever(self):
        logger.info('Starting chat bridge websocket server')
        async with websockets.serve(handle_websocket, self.cfg['bridge']['ip'], self.cfg['bridge']['port']):
            await asyncio.Future()
    
    async def set_auth_uuid(self, interaction: nextcord.Interaction, uuid):
        """ Sets a guild's auth UUID (after hash + salt) and responds to the interaction. """
        db = Database(interaction.guild, reason='Chat Bridge, set auth uuid for a guild')
        db.set('chat_bridge_uuid_hashed', bcrypt.hashpw(uuid, bcrypt.gensalt(12)))
        await interaction.send(f'**Successfully set new bridge UUID!**\nYou should now be able to start the other side of your bridge.')

    
    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        logger.info('Loaded cog chatbridge.py')

        await self.run_server_forever()
    
    @commands.Cog.listener()
    async def on_message(self, message: nextcord.Message):
        if message.guild.id in self.connections:
            if message.channel.id in self.connections[message.guild.id]: # nested to avoid KeyError
                attachments = []
                for file in message.attachments:
                    attachments.append(file.url)
                output = {
                    "origin": "internal",
                    "author": {
                        "name": message.author.display_name,
                        "username": message.author.name,
                        "id": message.author.id,
                        "profile": message.author.avatar.url
                    },
                    "message": {
                        "content": message.content,
                        "content_clean": message.clean_content,
                        "attachments": attachments, 
                        "timestamp": int( math.trunc(message.created_at.timestamp()) )
                    },
                    "authority": {
                        "uuid": self.internal_auth_uuid,
                        "guild": message.guild.id,
                        "channel": message.channel.id,
                    }
                }


    # Commands
    @nextcord.slash_command(description='Input key to allow chat bridge connections')
    async def bridge(self, interaction: nextcord.Interaction):
        db = Database(interaction.guild, reason='Slash command `/bridge`, check permission')
        if utility.is_mod(interaction.user, db) or interaction.user.id in db.fetch('admins'):
            await interaction.response.send_modal(modals.InputModal('Enable Chat Bridge', 'Paste connection UUID:', self.set_auth_uuid))
        else:
            await interaction.send(self.cfg['messages']['noperm'])
    

def setup(bot):
    with open("config/config.yml", "r") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
    if cfg['bridge']['enabled']:
        bot.add_cog(ChatBridge(bot))
        logger.debug('Setup cog "chatbridge"')
    else:
        logger.warning('Chat bridge disabled.')