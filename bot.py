#!/usr/bin/env python3

import nextcord
from nextcord.ext import commands
import os

import logging
import mysql.connector
import yaml

with open("config/config.yml", "r") as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

bot = commands.Bot()
sql = mysql.connector.connect(
    host=cfg["mysql"]["host"],
    user=cfg["mysql"]["user"],
    password=cfg["mysql"]["pass"],
    database=cfg["mysql"]["db"]
)
cursor = sql.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS admins (id BIGINT, permission INT)")

# messages (just for loading cogs commands)
noperm = cfg["messages"]["noperm"]
noperm_log = cfg["messages"]["noperm_log"]

# load from the table of admins
cursor.execute("SELECT * FROM admins")
admins = cursor.fetchall()

# Print to log when successfully logged in
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    logging.info(f'Logged in as {bot.user}')

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
                logging.debug(f"Listed cogs for {interaction.user}")
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
        logging.debug(noperm_log)

@bot.slash_command()
async def unload(interaction: nextcord.Interaction, extension):
    if interaction.user.id in admins:
        try:
            cogs_list = ''
            if extension is None:
                for filename in os.listdir('./cogs'):
                    if filename.endswith('.py'):
                        cogs_list += ( ' • ' + filename.strip('.py') + '\n')
                await interaction.send(f'Available Cogs:\n{cogs_list}')
                logging.debug(f"Listed cogs for {interaction.user}")
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
        logging.debug(noperm_log)

@bot.slash_command()
async def reload(interaction: nextcord.Interaction, extension):
    if interaction.user.id in admins:
        try:
            cogs_list = ''
            if extension is None:
                for filename in os.listdir('./cogs'):
                    if filename.endswith('.py'):
                        cogs_list += ( ' • ' + filename.strip('.py') + '\n')
                await interaction.send(f'Available Cogs:\n{cogs_list}')
                logging.debug(f"Listed cogs for {interaction.user}")
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
        logging.debug(noperm_log)

@bot.slash_command(description='[Admin] Stop the bot')
async def stop(interaction: nextcord.Interaction, extension):
    if interaction.user.id in admins:
        await interaction.send('**⚠️ Stopping the bot!**')
        logging.info(f'{interaction.user} stopped the bot.')
        exit(0)
    else:
        await interaction.response.send(noperm, ephemeral=True)
        cmd = 'stop'
        logging.debug(noperm_log)

# Load Cogs
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

# Run the Bot
bot.run('MTAzNTMyMzc1OTY4ODY3OTQ0NA.Gfbtej.DBm7Y82JguDyFjmEFoUaSzV30LslLj2xiMmwUA')
