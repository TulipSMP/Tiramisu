# 
# Tiramisu Discord Bot
# --------------------
# REST API Processing Library
# 
from logging42 import logger

import yaml
import uuid

def get_queue_file():
    with open('config/config.yml', 'r') as f:
        cfg = yaml.full_load(f)
    
    return cfg['api']['queue']

def add_request(guild: str, action: str, params: dict):
    """ Add API Request for Bot to process """
    file = get_queue_file()
    request = {
        'guild': guild,
        'action': action,
        'params': params,
        'fulfilled': False
    }
    with open(file, 'r') as f:
        queue = yaml.full_load(f)
    request_id = uuid.uuid4().hex
    queue[request_id] = request
    
    with open(file, 'w') as f:
        yaml.dump(queue, f)
    logger.debug(f'Added API Request to Queue with ID {request_id}: {str(request)}')

def prune_requests():
    """ Prune fulfilled API requests """
    logger.debug(f'Pruning fulfilled API requests...')
    file = get_queue_file()
    with open(file, 'r') as f:
        queue = yaml.full_load(f)
    count = 0
    for request in queue:
        if queue[request]['fulfilled']:
            del queue[request]
            count += 1
    with open(file, 'w') as f:
        yaml.dump(queue, file)
    del queue
    logger.debug(f'Pruned {count} fulfilled API requests.')

# TODO: func to fetch list of unprocessed api requests
