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

# Database
logger.info("Using Database Storage...")
import mysql.connector
sql = mysql.connector.connect(
    host=cfg["mysql"]["host"],
    user=cfg["mysql"]["user"],
    password=cfg["mysql"]["pass"],
    database=cfg["mysql"]["db"]
)
cursor = sql.cursor()

cursor.execute(f"CREATE TABLE IF NOT EXISTS admins (id BIGINT, permission INT);")

cursor.execute("SELECT id FROM admins;")
admins = cursor.fetchall()


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
# Pre requisite for subcommands
@nextcord.slash_command(description='List available Cogs',guild_ids=[TESTING_GUILD_ID])
async def cogs(self, interaction: nextcord.Interaction):
    cogs_list = ''
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            cogs_list += ( ' • ' + filename.strip('.py') + '\n')
    await interaction.send(f'Available Cogs:\n{cogs_list}')
    logger.debug(f"Listed cogs for {interaction.user}")
# Load Cogs
@cogs.subcommand(description="Load cogs", guild_ids=[TESTING_GUILD_ID])
async def load(interaction: nextcord.Interaction, extension=None):
    if interaction.user.id in admins:
        try:
            if extension is None:
                await interaction.send("Please specify a cog.", ephemeral=True)
            else:
                bot.load_extension(f'cogs.{extension}')
                await interaction.send(f'Loaded cog `{extension}`!')
        except nextcord.ext.commands.errors.ExtensionAlreadyLoaded:
            await interaction.send(f'The cog `{extension}` is already loaded.')
        except nextcord.ext.commands.errors.ExtensionNotFound:
            await interaction.send(f'The cog `{extension}` was not found.')
    else:
        await interaction.send(noperm, ephemeral=True)
        logger.debug(noperm_log)

# Unload Cogs
@cogs.subcommand(description="Unload cogs", guild_ids=[TESTING_GUILD_ID])
async def unload(interaction: nextcord.Interaction, extension=None):
    if interaction.user.id in admins:
        try:
            if extension is None:
                await interaction.send("Please specify a cog.", ephemeral=True)
            else:
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
@cogs.subcommand(description="Reload cogs", guild_ids=[TESTING_GUILD_ID])
async def reload(interaction: nextcord.Interaction, extension=None):
    if interaction.user.id in admins:
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
async def stop(interaction: nextcord.Interaction):
    if interaction.user.id in admins:
        await interaction.send('**⚠️ Stopping the bot!**')
        logger.info(f'{interaction.user} stopped the bot.')
        sys.exit("Stopping...")
    else:
        await interaction.send(noperm, ephemeral=True)
        logger.debug(noperm_log)

# Load Cogs
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

# Run the Bot
bot.run(bot_token)
