# 
# Tiramisu Discord Bot
# --------------------
# REST API Server
# 
from logging42 import logger

import yaml
import secrets

from aiohttp import web

from libs import requests_processor

def fetch_global_secret():
    with open("config/config.yml", "r") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

    try:
        with open(cfg['api']['secret'], 'r') as f:
            secret = f.readlines()[0].strip(' \n')
    except FileNotFoundError:
        secret = ''
    if secret == '':
        with open(cfg['api']['secret'], 'w') as f:
            secret = secrets.token_urlsafe(32)
            f.write(secret)
    
    return secret

async def server():
    """ Run the API Server """
    app = web.Application()
    app.add_routes(
        [
        web.post('/modlog', modlog),
        ]
    )
    
    web.run(app)

# Endpoints
async def modlog(request):
    """ Upload a Modlog Entry """
    # Load and Parse Data
    data = json.loads(request.data)
    try:
        instance_secret = data["instance_secret"]
        guild_secret = data["guild_secret"]
        guild_id = data["guild_id"]
        action = data["action"]
        user = data["user"]
        platform = data["platform"]
        reason = data["reason"]
        author = data["author"]
    except KeyError:
        return web.Response(text='Missing Required Arguments', status=400)

    # Authenticate
    if instance_secret != secret:
        return web.Response(text='Invalid Instance Secret', status=401)

    # Parse optional data
    if 'duration' in data:
        duration = data['duration']
    else:
        duration = None
    if 'notes' in data:
        notes = data["notes"]
    else:
        notes = None

    params = {
        'guild_secret': guild_secret,
        'action': action,
        'user': user,
        'platform': platform,
        'reason': reason,
        'author': author,
        'duration': duration,
        'notes': notes
    }
    requests_processor.add_request(guild_id, 'modlog', params)

    # Respond
    return web.Response(text='Added Request to Processing Queue', status=202)