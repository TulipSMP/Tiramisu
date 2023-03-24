from logging42 import logger
import nextcord
from nextcord.ext import commands
import yaml
from libs.database import Database
from typing import Optional

class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open("config/config.yml", "r") as ymlfile:
            self.cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
    
    with open("config/config.yml", "r") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
    TESTING_GUILD_ID = cfg['discord']['testing_guild']

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        logger.info('Loaded cog utilities.py')

    # Commands
    @nextcord.slash_command(description="Get the game server IP", guild_ids=[TESTING_GUILD_ID])
    async def ip(self, interaction: nextcord.Interaction):
        db = Database(interaction.guild, reason='Slash command `/ip`')
        ip = db.fetch('ip_address')
        text = db.fetch('ip_text')
        game = db.fetch('ip_game')
        warn = ''
        if ip == 'none':
            warn += '\nAsk the admins to change the setting `ip_address`'
        if text == 'none':
            text = ''
            warn += '\nAsk the admins to change the setting `ip_text` to show a description.'
        if game == 'none':
            warn += '\nAsk the admins to change the setting `ip_game` to which game their server is for.'
        await interaction.send(f'**{game.title()} Server IP:** `{ip}`\n{text}{warn}')
    
    @nextcord.slash_command(description='Give all users a specific role', guild_ids=[TESTING_GUILD_ID])
    async def addrole(self, interaction: nextcord.Interaction,
        role: Optional[nextcord.Role] = nextcord.SlashOption(description='What role to give everyone', required=True)):
        db = Database(interaction.guild, reason='Slash command `/addrole`')
        if interaction.user.id in db.fetch('admins'):
            if interaction.guild.member_count >= 10:
                await interaction.response.defer()
            times = 0
            try:
                for user in interaction.guild.humans:
                    await user.add_roles(role, atomic=True, reason=f'{interaction.user.name}#{interaction.user.discriminator} used the `/addrole` command')
                    times += 1
            except nextcord.errors.NotFound:
                await interaction.send(f'That is not a valid role!')
                return
            await interaction.send(f'Added role `@{role.name}` to all {times} users.')            
        else:   
            await interaction.send(self.cfg['messages']['noperm'], ephemeral=True)
    
    @nextcord.slash_command(description='Remove a specific role from all users', guild_ids=[TESTING_GUILD_ID])
    async def delrole(self, interaction: nextcord.Interaction,
        role: Optional[nextcord.Role] = nextcord.SlashOption(description='What role to remove from everyone', required=True)):
        db = Database(interaction.guild, reason='Slash command `/delrole`')
        if interaction.user.id in db.fetch('admins'):
            if interaction.guild.member_count >= 10:
                await interaction.response.defer()
            times = 0
            try:
                for user in interaction.guild.humans:
                    await user.remove_roles(role, atomic=True, reason=f'{interaction.user.name}#{interaction.user.discriminator} used the `/delrole` command')
                    times += 1
            except nextcord.errors.NotFound:
                await interaction.send(f'That is not a valid role!')
                return
            await interaction.send(f'Removed role `@{role.name}` from all {times} users.')            
        else:   
            await interaction.send(self.cfg['messages']['noperm'], ephemeral=True)


def setup(bot):
    bot.add_cog(Utilities(bot))
    logger.debug('Setup cog "utilities"')