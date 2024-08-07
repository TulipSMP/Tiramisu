#!/usr/bin/env python3
#
# Tiramisu Discord Bot
# --------------------
# Main Python File
#

from logging42 import logger

import nextcord
from nextcord.ext import commands

import os
import sys
import sqlite3
import yaml
import shutil
from typing import Optional

from libs.database import Database
from libs import utility, extensions

# Ensure Config exists:
if os.path.exists('config/config.yml'):
    logger.info('Successfully found config/config.yml!')
    utility.verify_config() # and verify it
else:
    try:
        shutil.copyfile('config/exampleconfig.yml','config/config.yml')
        logger.critical(f'Bot is not configured! Please edit config/config.yml')
        sys.exit(1)
    except BaseException as e:
        logger.critical(f'{e}: Could not find config file! Try re-cloning the git repository.')
        sys.exit(1)

with open("config/config.yml", "r") as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
    cfg_obfuscated = f'{cfg}'.replace(cfg["discord"]["token"], "[ AUTOMATICALLY REDACTED ]")
    logger.info(f'Successfully loaded config/config.yml: {cfg_obfuscated}')

TESTING_GUILD_ID=cfg["discord"]["testing_guild"]

# Configure Logging
if not cfg['debug']:
    # Only show "INFO" and above if not in debug mode
    logger.remove(1) # Remove default logger
    logger.add(sys.stdout, level="INFO") # Add "INFO" and above logger

# Load things from cfg
bot_token = cfg["discord"]["token"]
# messages (just for loading cogs commands)
noperm = cfg["messages"]["noperm"]
noperm_log = cfg["messages"]["noperm_log"]

## INTENTS
intents = nextcord.Intents.all()

## LOGIN
bot = commands.Bot(intents=intents)

# Print to log when successfully logged in
@bot.event
async def on_ready():
    logger.info(f'Logged in as {bot.user}')

# Load Commands

# List Cogs
@bot.slash_command(description='Cog actions', guild_ids=[TESTING_GUILD_ID])
async def cogs(interaction: nextcord.Interaction):
    pass # Setup for following subcommands

@cogs.subcommand(description='List cogs')
async def list(interaction: nextcord.Interaction):
    if interaction.user.id in cfg['discord']['co_owners'] or interaction.user.id == cfg['discord']['owner']:
        cogs_list = ''
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                cogs_list += ( ' • ' + filename[:-3] + '\n')
        await interaction.send(f'Available Cogs:\n{cogs_list}')
        logger.debug(f"Listed cogs for {interaction.user}")
    else:
        await interaction.send(noperm, ephemeral=True)

# Load Cogs
@cogs.subcommand(description="Load cogs")
async def load(interaction: nextcord.Interaction,
    extension: Optional[str] = nextcord.SlashOption(description='What cog to load', required=True)):
    if interaction.user.id in cfg['discord']['co_owners'] or interaction.user.id == cfg['discord']['owner']:
        try:
            bot.load_extension(f'cogs.{extension}')
            await interaction.send(f'Loaded cog `{extension}`!')
        except nextcord.ext.commands.errors.ExtensionAlreadyLoaded:
            await interaction.send(f'The cog `{extension}` is already loaded.')
        except nextcord.ext.commands.errors.ExtensionNotFound:
            await interaction.send(f'The cog `{extension}` was not found.')
    else:
        await interaction.send(noperm, ephemeral=True)

# Unload Cogs
@cogs.subcommand(description="Unload cogs")
async def unload(interaction: nextcord.Interaction,
    extension: Optional[str] = nextcord.SlashOption(description='What cog to unload', required=True)):
    if interaction.user.id in cfg['discord']['co_owners'] or interaction.user.id == cfg['discord']['owner']:
        try:
            bot.unload_extension(f'cogs.{extension}')
            await interaction.send(f'Unloaded cog `{extension}`!')
        except nextcord.ext.commands.errors.ExtensionNotLoaded:
            await interaction.send(f'The cog `{extension}` is not loaded.')
        except nextcord.ext.commands.errors.ExtensionNotFound:
            await interaction.send(f'The cog `{extension}` was not found.')
    else:
        await interaction.send(noperm, ephemeral=True)

# Reload Cogs
@cogs.subcommand(description="Reload cogs")
async def reload(interaction: nextcord.Interaction, 
    extension: Optional[str] = nextcord.SlashOption(description='What cog to load', required=True)):
    if interaction.user.id in cfg['discord']['co_owners'] or interaction.user.id == cfg['discord']['owner']:
        try:
            bot.reload_extension(f'cogs.{extension}')
            await interaction.send(f'Reloaded cog `{extension}`!')
        except nextcord.ext.commands.errors.ExtensionNotLoaded:
            await interaction.send(f'The cog `{extension}` is not loaded.')
        except nextcord.ext.commands.errors.ExtensionNotFound:
            await interaction.send(f'The cog `{extension}` was not found!')
    else:
        await interaction.send(noperm, ephemeral=True)

# Stop the Bot
@bot.slash_command(description='Stop the bot', guild_ids=[TESTING_GUILD_ID])
async def stop(interaction: nextcord.Interaction):
    if interaction.user.id in cfg['discord']['co_owners'] or interaction.user.id == cfg['discord']['owner']:
        await interaction.send('**🛑 Stopping the bot!**')
        logger.info(f'{interaction.user.name} [{interaction.user.id}] stopped the bot.')
        sys.exit(0)
    else:
        await interaction.send(noperm, ephemeral=True)

# Load Cogs
loaded_cogs = []
for filename in os.listdir('./cogs'):
    if filename.endswith('.py') and filename not in cfg['cog_dontload']:
        bot.load_extension(f'cogs.{filename[:-3]}')
    loaded_cogs.append(f'{filename[:-3]}')
logger.info(f'Loaded Cogs: {loaded_cogs}')

# Load Extensions
loaded_exts = []
for ext in extensions.get_ext_list():
    bot.load_extension(f'ext.{ext}')
    loaded_exts.append(ext)
logger.info(f'Loaded Extensions: {loaded_exts}')

# Run the Bot
bot.run(bot_token)
