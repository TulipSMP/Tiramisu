#!/usr/bin/env python3
from logging42 import logger
import nextcord
from nextcord.ext import commands
import os
import sys
import sqlite3
import yaml
from shutil import copyfile

with open("config/config.yml", "r") as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

bot = commands.Bot()

TESTING_GUILD_ID=cfg["discord"]["testing_guild"]

# Ensure Config exists:
if os.path.exists('config/config.yml'):
    logger.debug('Successfully found config/config.yml')
else:
    try:
        shutil.copyfile('config/exampleconfig.yml','config/config.yml')
        logger.error(f'Bot is not configured! Please edit config/config.yml')
    except BaseException as e:
        logger.critical(f'{e}: Could not find config file! Try re-cloning the git repository.')
        sys.exit(1)

# Database
logger.info("Using Database Storage...")
if cfg["storage"] == "sqlite":
    sql = sqlite3.connect('storage.db')
    cursor = sql.cursor()
else:
    import mysql.connector
    sql = mysql.connector.connect(
        host=cfg["mysql"]["host"],
        user=cfg["mysql"]["user"],
        password=cfg["mysql"]["pass"],
        database=cfg["mysql"]["db"]
    )
    cursor = sql.cursor()

# Load Adminsitrators from DB
cursor = sql.cursor()
cursor.execute(f"CREATE TABLE IF NOT EXISTS admins (id BIGINT, permission INT);")
cursor.execute("SELECT id FROM admins;")
admins_raw = cursor.fetchall()
### And parse the convoluted output
admins = []
for admin_id in admins_raw:
    admin_str = f'{admin_id}'
    admin_new = admin_str.replace(',', '')
    admin_new = admin_new.replace('(', '')
    admin_new = admin_new.replace(')', '')
    admins.append(admin_new)


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

# List Cogs
@bot.slash_command(description='List cogs', guild_ids=[TESTING_GUILD_ID])
async def cogs(interaction: nextcord.Interaction):
    if interaction.user.id in cfg['discord']['co_owners'] or interaction.user.id == cfg['discord']['owner']:
        cogs_list = ''
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                cogs_list += ( ' • ' + filename.strip('.py') + '\n')
        await interaction.send(f'Available Cogs:\n{cogs_list}')
        logger.debug(f"Listed cogs for {interaction.user}")
    else:
        await interaction.send(noperm, ephemeral=True)
        logger.debug(noperm_log)

# Load Cogs
@bot.slash_command(description="Load cogs", guild_ids=[TESTING_GUILD_ID])
async def load(interaction: nextcord.Interaction, extension=None):
    if interaction.user.id in cfg['discord']['co_owners'] or interaction.user.id == cfg['discord']['owner']:
        try:
            if extension is None:
                await interaction.send("Please specify a cog.", ephemeral=True)
            else:
                bot.load_extension(f'cogs.{extension}', cursor)
                await interaction.send(f'Loaded cog `{extension}`!')
        except nextcord.ext.commands.errors.ExtensionAlreadyLoaded:
            await interaction.send(f'The cog `{extension}` is already loaded.')
        except nextcord.ext.commands.errors.ExtensionNotFound:
            await interaction.send(f'The cog `{extension}` was not found.')
    else:
        await interaction.send(noperm, ephemeral=True)
        logger.debug(noperm_log)

# Unload Cogs
@bot.slash_command(description="Unload cogs", guild_ids=[TESTING_GUILD_ID])
async def unload(interaction: nextcord.Interaction, extension):
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
        logger.debug(noperm_log)

# Reload Cogs
@bot.slash_command(description="Reload cogs", guild_ids=[TESTING_GUILD_ID])
async def reload(interaction: nextcord.Interaction, extension=None):
    if interaction.user.id in cfg['discord']['co_owners'] or interaction.user.id == cfg['discord']['owner']:
        try:
            if extension is None:
                await interaction.send("Please specify a cog.", ephemeral=True)
            else:
                bot.reload_extension(f'cogs.{extension}')
                await interaction.send(f'Reloaded cog `{extension}`!')
        except nextcord.ext.commands.errors.ExtensionNotLoaded:
            await interaction.send(f'The cog `{extension}` is not loaded.')
        except nextcord.ext.commands.errors.ExtensionNotFound:
            await interaction.send(f'The cog `{extension}` was not found!')
    else:
        await interaction.send(noperm, ephemeral=True)
        logger.debug(noperm_log)

# Stop the Bot
@bot.slash_command(description='Stop the bot', guild_ids=[TESTING_GUILD_ID])
async def stop(interaction: nextcord.Interaction, emergency=False):
    if interaction.user.id in cfg['discord']['co_owners'] or interaction.user.id == cfg['discord']['owner']:
        if emergency:
            os.system(f"sed -i 's/Restart=always/Restart=no/g' /home/{os.getenv('USER')}/.config/systemd/user/tiramisu.service")
        await interaction.send('**⚠️ Stopping the bot!**')
        logger.info(f'{interaction.user} stopped the bot.')
        sys.exit("Stopping...")
    else:
        await interaction.send(noperm, ephemeral=True)
        logger.debug(noperm_log)

# Load Cogs
loaded_cogs = []
for filename in os.listdir('./cogs'):
    if filename.endswith('.py') and filename not in cfg['cog_dontload']:
        bot.load_extension(f'cogs.{filename[:-3]}')
    loaded_cogs.append(f'{filename[:-3]}')
logger.info(f'Loaded Cogs: {loaded_cogs}')

# Run the Bot
bot.run(bot_token)
