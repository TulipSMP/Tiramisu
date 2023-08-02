# 
# Tiramisu Discord Bot
# --------------------
# Chat Bridge
# 
from logging42 import logger

import asyncio
import json
import nextcord
from nextcord.ext import commands
import websockets
import yaml

from libs.database import Database
from libs import utility, moderation

from typing import Optional

class ChatBridge(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        with open("config/config.yml", "r") as ymlfile:
            self.cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

        # Start the WebSocket server in the background
        self.websocket_server_task = self.bot.loop.create_task(self.start_websocket_server())

    async def start_websocket_server(self):
        async def broadcast_info(message, guild_id):
            if self.cfg['debug']:
                logger.success(f"Broadcasting to guild ID: {guild_id}, Message: {message}")

        async def handle_connection(websocket, path):
            try:
                # Receive guild_id from the client
                guild_id = await websocket.recv()

                db = Database(guild_id, reason='Chat Bridge, fetch settings')
                ip_address = db.fetch('ip_address')
                private_key = db.fetch('private_key')

                if path != f"/{ip_address}":
                    return

                async for message in websocket:
                    try:
                        message_data = json.loads(message)
                        user_id = message_data.get('user_id')
                        username = message_data.get('username')
                        nickname = message_data.get('nickname')
                        top_role = message_data.get('top_role')
                        top_role_color = message_data.get('top_role_color')
                        message_content = message_data.get('message')

                        info = {
                            'username': username,
                            'nickname': nickname,
                            'top_role': top_role,
                            'top_role_color': top_role_color,
                            'message': message_content
                        }
                        await broadcast_info(json.dumps(info), guild_id)

                    except json.JSONDecodeError:
                        pass

            except websockets.exceptions.ConnectionClosedOK:
                # Connection was closed cleanly
                pass

        server = await websockets.serve(handle_connection, "localhost", 8765)
        logger.info("WebSocket server started.")

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        logger.info('Loaded cog chat_bridge.py!')


def setup(bot):
    bot.add_cog(ChatBridge(bot))
    logger.debug('Setup cog "chat_bridge"')
