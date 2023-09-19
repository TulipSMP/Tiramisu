# 
# Tiramisu Discord Bot
# --------------------
# Extension Support
# 
from logging42 import logger

import nextcord

from typing import List

import importlib
import yaml
import os

def get_ext_list():
    """ Fetch a list of all extensions """
    with open('config/config.yml') as file:
        cfg = yaml.full_load(file)

    extensions = []
    for filename in os.listdir('./ext'):
        if filename.endswith('.py') and filename not in cfg['cog_dontload']:
            extensions.append(filename.removesuffix('.py'))

def get_settings(extensions: List[str]):
    """ Fetch a list of settings added by given extensions (by name) """
    settings = []

    for ext_name in extensions:
        ext = importlib.import_module(f'ext.{ext_name}')
        try:
            if isinstance(ext.settings, list):
                settings += ext.settings
        except:
            continue
    
    return settings

def get_settings_hidden(extensions: List[str]):
    """ Fetch a list of hidden settings added by given extensions (by name) """
    settings_hidden = []

    for ext_name in extensions:
        ext = importlib.import_module(f'ext.{ext_name}')
        try:
            if isinstance(ext.settings_hidden, list):
                settings_hidden += ext.settings_hidden
        except:
            continue
    
    return settings_hidden
