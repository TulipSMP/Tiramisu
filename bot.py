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

TESTING_GUILD_ID=cfg["discord"]["testing_guild"]

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
        logger.debug("Made dir './config/storage'.")
    except FileExistsError:
        logger.debug("Local storage already exists.")
    try:
        os.mknod("./config/storage/db.yml")
        logger.debug("Made file './config/storage/db.yml'.")
    except FileExistsError:
        logger.debug("'./config/storage/db.yml' already exists.")
    # Create db.yml
    with open("./config/storage/db.yml", "r") as db_r_ymlfile:
            db = yaml.load(db_r_ymlfile, Loader=yaml.FullLoader)
            logger.debug("Opened db.yml (for reading)")
    # Be able to save it later
    def localdb_save(load=db, context='None given'):
        try:
            with open("./config/storage/db.yml", "w") as db_w_ymlfile:
                    db_w = yaml.safe_dump(load, db_w_ymlfile)
                    logger.info(f"Saved db.yml for reason: '{context}'.")
            return True
        except Exception as e:
            logger.error(f"localdb_save() UNSUCCESSFUL!")
            logger.error(f"localdb_save() FAILED WITH ERROR '{e}'!")
            return False
    # Ensure all tables exist
    logger.info("Checking if tables exist...")
    try:
        for table in cfg["mysql"]["tables"]:
            for k in db:
                if table in k:
                    logger.debug(f"Table '{table}' exists.")
                else:
                    with open('./config/storage/db.yml', 'r') as db_old:
                        yaml = str(db_old) + '\n' + table + ': []\n'
                    db_new = yaml.safe_load(yaml)
                    localdb_save(load=db_new, context='Adding table ' + table + '.')
                    logger.debug(f"Added table {table}.")
    except AttributeError:
        logger.debug('db.yml is empty. Creating tables...')
        new_yaml = ''
        for table in cfg["mysql"]["tables"]:
            new_yaml += f"\n{table}: []\n"
            localdb_save(context=f"Adding table {table}", load=new_yaml)
    logger.info("Tables check Done.")



# load from the table of admins
if cfg["storage"]["db"]:
    cursor.execute("SELECT * FROM admins")
    admins = cursor.fetchall()
else:
    try:
        admins = db["admins"]
    except TypeError:
        logger.debug("In 'db.yml', table 'admins' is either empty or is invalid.")
        admins = []

# Load things from cfg
bot_token = cfg["discord"]["token"]
# messages (just for loading cogs commands)
noperm = cfg["messages"]["noperm"]
noperm_log = cfg["messages"]["noperm_log"]

# Print to log when successfully logged in
@bot.event
async def on_ready():
    logger.info(f'Logged in as {bot.user}')

# Load Commands
# Load Cogs
@bot.slash_command(description="[Admin] Load cogs", guild_ids=[TESTING_GUILD_ID])
async def load(interaction: nextcord.Interaction, extension=None):
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
        await interaction.send(noperm, ephemeral=True)
        cmd = 'load'
        logger.debug(noperm_log)

# Unload Cogs
@bot.slash_command(description="[Admin] Unload cogs", guild_ids=[TESTING_GUILD_ID])
async def unload(interaction: nextcord.Interaction, extension=None):
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
        await interaction.send(noperm, ephemeral=True)
        cmd = 'unload'
        logger.debug(noperm_log)

# Reload Cogs
@bot.slash_command(description="[Admin] Reload cogs", guild_ids=[TESTING_GUILD_ID])
async def reload(interaction: nextcord.Interaction, extension=None):
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
        await interaction.send(noperm, ephemeral=True)
        cmd = 'reload'
        logger.debug(noperm_log)

# Stop the Bot
@bot.slash_command(description='[Admin] Stop the bot', guild_ids=[TESTING_GUILD_ID])
async def stop(interaction: nextcord.Interaction):
    if interaction.user.id in admins:
        await interaction.send('**⚠️ Stopping the bot!**')
        if not cfg["storage"]["db"]:
            localdb_save(context="Stop Command")
        logger.info(f'{interaction.user} stopped the bot.')
        sys.exit("Stopping...")
    else:
        await interaction.send(noperm, ephemeral=True)
        cmd = 'stop'
        logger.debug(noperm_log)

# Load Cogs
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')
# Load Cogs from enabled Submodules
if cfg["cog_submodules"]["use_cog_submodules"]:
    for submodule in cfg["cog_submodules"]["cog_submodules"]:
        for filename in os.listdir(f'./cogs/{submodule}'):
            if filename.endswith(".py"):
                bot.load_extension(f"cogs.{submodule}.{filename[:-3]}")

# Run the Bot
bot.run(bot_token)
