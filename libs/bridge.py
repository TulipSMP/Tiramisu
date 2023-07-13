# 
# Tiramisu Discord Bot
# --------------------
# Chat Bridge Classes
# 
from logging42 import logger

import asyncio
import yaml
import json
import uuid
import inspect
import websockets

import nextcord
from nextcord.ext import commands

from libs.database import Database
from libs import utility

# Exception Classes
class NoBridgeUUID(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class BridgeAlreadyRunning(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Bridge:
    def __init__(self, bot: nextcord.Bot, guild: nextcord.Guild):
        """ Chat Bridge Instance """
        db = Database(guild, reason='Bridge, create bridge')

        self.bot = bot
        self.guild = guild
        self.running = False

        self._listeners = []
        self._queue = []
        self.uuid = self.get_uuid()

        with open('config/config.yml', 'r') as file:
            self.cfg = yaml.load(file, Loader=yaml.FullLoader)


        if db.fetch('bridge_uuid') == 'none':
            db.set('bridge_uuid', str(uuid.uuid4()))
        
        self.forwarding_secret = f'X-Tiramisu-Forward-{uuid.uuid4()}: '
    
    def set_uuid(self, uuid):
        """ Set the UUID for this Bridge """
        if self.running:
            raise BridgeAlreadyRunning
        else:
            db = Database(self.guild, reason='Bridge, set uuid')
            db.set('bridge_uuid', uuid)
            self.uuid = uuid
            db.close()
    
    def get_uuid(self):
        """ Get the UUID for this Bridge """
        db = Database(self.guild, reason='Bridge, get uuid')
        self.uuid = db.fetch('bridge_uuid')
        return self.uuid
    
    def on_external_message(self, func):
        """ Register function to be run when a message comes in over the websocket.
        The registered function will be passed the raw JSON we recieved. """
        self._listeners.append(func)
        return func

    async def _handle_incoming_message(self, websocket):
        """ Internal use Only. Handles incoming websocket messages. """
        if self._queue != []:
            for message in self._queue:
                await websocket.send(message)
                logger.debug(f'Outgoing message from bridge {self.get_uuid}: {msg}')
        else:
            msg = await websocket.recv()
            logger.debug(f'Incoming message on Bridge {self.get_uuid()}: {msg}')


            try:
                msg = json.loads(msg)
            except json.decoder.JSONDecodeError:
                return
            
            for func in self._listeners:
                if inspect.isawaitable(func):
                    await func(self.guild.id, msg)
                else:
                    func(msg)
    

    async def run(self):
        """ Run the Bridge Server Forever """
        uuid = self.get_uuid()
        address = f"{self.cfg['bridge']['ip']}/bridge/{uuid}"
        port = self.cfg['bridge']['port']
        self.running = True
        
        logger.info(f'Starting chat bridge {uuid}')

        async with websockets.serve(self._handle_incoming_message, address, port):
            await asyncio.Future() # Run Forever
    
    def send_bridge_message(self, message: nextcord.Message):
        """ Send a message into the websocket """
        msg = {
            "author": {
                "name": message.author.name,
                "display": message.author.display_name,
                "avatar": message.author.display_avatar.url
            },
            "message": {
                "content": message.clean_content,
                "content_raw": message.content,
                "timestamp": int(message.created_at.timestamp() * 1000000),
                "attachments": utility.attachments_to_url_list(message)
            },
            "destination": {
                "uuid": self.get_uuid(),
                "channel": message.channel.id
            }
        }
        self._queue.append(msg)
        logger.debug(f'Added message to Bridge {self.uuid} queue: {msg}')



    
