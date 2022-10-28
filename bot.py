#!/usr/bin/env python3

import nextcord
from nextcord.ext import commands
import os


bot = commands.Bot()

# messages (just for loading cogs commands)
noperm = f'No permission!'

# Print to log when successfully logged in
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

# Load Commands
@bot.slash_command()
async def load(interaction: nextcord.Interaction, extension):
    if interaction.user.get_role(staff):
        try:
            bot.load_extension(f'cogs.{extension}')
            msg=f'Loaded cog `{extension}`!'
            await interaction.send(msg)
            print(msg)
        except nextcord.ext.commands.errors.ExtensionAlreadyLoaded:
            await interaction.send(f'The cog `{extension}` is already loaded.')
        except nextcord.ext.commands.errors.ExtensionNotFound:
            await interaction.send(f'The cog `{extension}` was not found.')
    else:
        await interaction.response.send(noperm, ephemeral=True)

@bot.slash_command()
async def unload(interaction: nextcord.Interaction, extension):
    if interaction.user.get_role(staff):
        try:
            bot.unload_extension(f'cogs.{extension}')
            msg=f'Unloaded cog `{extension}`!'
            await interaction.send(msg)
            print(msg)
        except nextcord.ext.commands.errors.ExtensionNotLoaded:
            await interaction.send(f'The cog `{extension}` is not loaded.')
        except nextcord.ext.commands.errors.ExtensionNotFound:
            await interaction.send(f'The cog `{extension}` was not found.')
    else:
        await interaction.response.send(noperm, ephemeral=True)

@bot.slash_command()
async def reload(interaction: nextcord.Interaction, extension):
    if interaction.user.get_role(staff):
        try:
            bot.reload_extension(f'cogs.{extension}')
            msg=f'Reloaded cog `{extension}`!'
            await interaction.send(msg)
            print(msg)
        except nextcord.ext.commands.errors.ExtensionNotLoaded:
            await interaction.send(f'The cog `{extension}` is not loaded.')
        except nextcord.ext.commands.errors.ExtensionNotFound:
            await interaction.send(f'The cog `{extension}` was not found!')
    else:
        await interaction.response.send(noperm, ephemeral=True)

# Load Cogs
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

# Run the Bot
bot.run('MTAzNTMyMzc1OTY4ODY3OTQ0NA.Gfbtej.DBm7Y82JguDyFjmEFoUaSzV30LslLj2xiMmwUA')
