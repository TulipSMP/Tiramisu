#!/usr/bin/env python3

from logging42 import logger

import nextcord
from nextcord.ext import commands
import os
import sys

import yaml

with open("config/config.yml", "r") as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

bot = commands.Bot()

# Database, if used
if cfg["storage"]["db"]:
    logger.info("Using Database Storage...")
    import mysql.connector
    sql = mysql.connector(
        host=cfg["mysql"]["host"],
        user=cfg["mysql"]["user"],
        password=cfg["mysql"]["pass"],
        database=cfg["mysql"]["db"]
    )
    cursor = sql.cursor()

    for table in cfg["mysql"]["tables"]:
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table} (id BIGINT, permission INT)")
# If not used, create local stuff
else:
    logger.info("Using Local Storage...")
    try:
        os.mkdir("./config/storage/")
    except FileExistsError:
        logger.debug("Local storage already exists.")
    # Dict for tables
    # Ensure all ttableables exist
    for table in cfg["mysql"]["tables"]:
        if os.path.exists(f"./config/storage/{table}.yml"):
            logger.debug(f"Local table {table} already exists.")
        else:
            with open(f"./config/storage/{table}.yml") as :
                0
        counter += 1

# messages (just for loading cogs commands)
noperm = cfg["messages"]["noperm"]
noperm_log = cfg["messages"]["noperm_log"]

# load from the table of admins
cursor.execute("SELECT * FROM admins")
admins = cursor.fetchall()

# Load token from cfg
bot_token = cfg["discord"]["token"]

# Print to log when successfully logged in
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    logger.info(f'Logged in as {bot.user}')

# Load Commands
@bot.slash_command(description="[Admin] Load cogs")
async def load(interaction: nextcord.Interaction, extension):
    if interaction.user.id in admins:
        try:
            cogs_list = ''
            if extension is None:
                for filename in os.listdir('./cogs'):
                    if filename.endswith('.py'):
                        cogs_list += ( ' • ' + filename.strip('.py') + '\n')
                await interaction.send(f'Available Cogs:\n{cogs_list}')
                logger.debug(f"Listed cogs for {interaction.user}")
            else:
                bot.load_extension(f'cogs.{extension}')
                await interaction.send(f'Loaded cog `{extension}`!')
        except nextcord.ext.commands.errors.ExtensionAlreadyLoaded:
            await interaction.send(f'The cog `{extension}` is already loaded.')
        except nextcord.ext.commands.errors.ExtensionNotFound:
            await interaction.send(f'The cog `{extension}` was not found.')
    else:
        await interaction.response.send(noperm, ephemeral=True)
        cmd = 'load'
        logger.debug(noperm_log)

@bot.slash_command(description="[Admin] Unload cogs")
async def unload(interaction: nextcord.Interaction, extension):
    if interaction.user.id in admins:
        try:
            cogs_list = ''
            if extension is None:
                for filename in os.listdir('./cogs'):
                    if filename.endswith('.py'):
                        cogs_list += ( ' • ' + filename.strip('.py') + '\n')
                await interaction.send(f'Available Cogs:\n{cogs_list}')
                logger.debug(f"Listed cogs for {interaction.user}")
            else:
                bot.unload_extension(f'cogs.{extension}')
                await interaction.send(f'Unloaded cog `{extension}`!')
        except nextcord.ext.commands.errors.ExtensionNotLoaded:
            await interaction.send(f'The cog `{extension}` is not loaded.')
        except nextcord.ext.commands.errors.ExtensionNotFound:
            await interaction.send(f'The cog `{extension}` was not found.')
    else:
        await interaction.response.send(noperm, ephemeral=True)
        cmd = 'unload'
        logger.debug(noperm_log)

@bot.slash_command(description="[Admin] Reload cogs")
async def reload(interaction: nextcord.Interaction, extension):
    if interaction.user.id in admins:
        try:
            cogs_list = ''
            if extension is None:
                for filename in os.listdir('./cogs'):
                    if filename.endswith('.py'):
                        cogs_list += ( ' • ' + filename.strip('.py') + '\n')
                await interaction.send(f'Available Cogs:\n{cogs_list}')
                logger.debug(f"Listed cogs for {interaction.user}")
            else:
                bot.reload_extension(f'cogs.{extension}')
                await interaction.send(f'Reloaded cog `{extension}`!')
        except nextcord.ext.commands.errors.ExtensionNotLoaded:
            await interaction.send(f'The cog `{extension}` is not loaded.')
        except nextcord.ext.commands.errors.ExtensionNotFound:
            await interaction.send(f'The cog `{extension}` was not found!')
    else:
        await interaction.response.send(noperm, ephemeral=True)
        cmd = 'reload'
        logger.debug(noperm_log)

@bot.slash_command(description='[Admin] Stop the bot')
async def stop(interaction: nextcord.Interaction, extension):
    if interaction.user.id in admins:
        await interaction.send('**⚠️ Stopping the bot!**')
        logger.info(f'{interaction.user} stopped the bot.')
        sys.exit("Stopping...")
    else:
        await interaction.response.send(noperm, ephemeral=True)
        cmd = 'stop'
        logger.debug(noperm_log)

# Load Cogs
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')
# Load Cogs from enabled Submodules
if cfg["tiramisu"]["use_cog_submodules"]:
    for submodule in cfg["cog_submodules"]["cog_submodules"]:
        for filename in os.listdir(f'./cogs/{submodule}'):
            if filename.endswith(".py"):
                bot.load_extension(f"cogs.{submodule}.{filename[:-3]}")

# Run the Bot
bot.run(bot_token)
