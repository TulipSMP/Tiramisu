# 
# Tiramisu Discord Bot
# --------------------
# Adminstrator Management
# 
from logging42 import logger
import nextcord
from nextcord.ext import commands
import yaml
from typing import Optional

from libs.database import Database
from libs import utility

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Load Yaml
        with open("config/config.yml", "r") as ymlfile:
            cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
        self.cfg = cfg

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        logger.info('Loaded cog admin.py')

    # Commands
    @nextcord.slash_command()
    async def admin(self, interaction: nextcord.Interaction):
        pass
        # This command is to set up the following as subcommands
    
    # Add a guild administrator
    @admin.subcommand(description="Add an administrator")
    async def add(self, interaction: nextcord.Interaction, user: Optional[nextcord.Member] = nextcord.SlashOption(description='Who to grant administrative privileges to', required=True)):
        db = Database(interaction.guild, reason='Slash command `/admin add`')
        if interaction.user.id == interaction.guild.owner_id or interaction.user.id in db.fetch('admins') or interaction.user.guild_permissions.administrator:
            admins = db.fetch('admins')
            try:
                if user.id in admins:
                    await interaction.send(f'`{user.name}` is already an admin!')
                else:
                    if db.set('admin', user.id):
                        logger.debug(f'{interaction.user.name} added {user.name} as bot administrator')
                    await interaction.send(f"Added {user.mention} as an admin.")
            except Exception as ex:
                await interaction.send(utility.error_unexpected(ex), ephemeral=True)
            db.close()
        else:
            await interaction.send(self.cfg["messages"]["noperm"], ephemeral=True)
    
    # List administrators
    @admin.subcommand(description='List administrators')
    async def list(self, interaction: nextcord.Interaction, 
        mention_admins: Optional[bool] = nextcord.SlashOption(description='Whether or not to ping admins in the returned message', required=False, default=False,
            choices={'Yes':True, 'No':False})):
        db = Database(interaction.guild, reason='Slash command `/admin list`')
        if interaction.user.id == interaction.guild.owner_id or interaction.user.id in db.fetch('admins')  or interaction.user.guild_permissions.administrator:
            msg = f'**Registered Administrators:**\n'
            try:
                msg_admins = ''
                for admin in db.fetch('admins'):
                    if mention_admins:
                        msg_admins += f'• <@{admin}> `{admin}`\n'
                    else:
                        user = self.bot.get_user(int(admin))
                        if user != None:
                            try:
                                if user.name == user.display_name:
                                    user_display = f'{user.name}#{user.discriminator}'
                                else:
                                    user_display = f'{user.name}#{user.discriminator} *({user.display_name})*'
                            except:
                                if user.name == user.display_name:
                                    user_display = f'{user.name}'
                                else:
                                    user_display = f'{user.name} *({user.display_name})*'
                        else:
                            user_display = ''
                        msg_admins += f'• {user_display} `{admin}`\n'
                logger.debug(f"Listed administrators for {interaction.user.name} ({interaction.user.id})")
                if msg_admins == '':
                    msg = '**No Registered Administrators.**\nThe server owner can add admins with the `/admin add` command.'
                await interaction.send(msg + msg_admins)
            except db.current_database.OperationalError:
                logger.critical(f'OperationalError in `/admin list` for guild {db.guild.id}')
                await interaction.send(utility.error_unexpected('OperationalError: either table does not exist, or database could not be accessed!'), ephemeral=True)
            except Exception as ex:
                await interaction.send(utility.error_unexpected(ex), ephemeral=True)
                logger.error(f'Failed to fetch list of admins for guild {db.guild.id}! Error: {ex}', exc_info=True)
            db.close()
        else:
            await interaction.send(self.cfg["messages"]["noperm"], ephemeral=True)
            logger.debug(self.cfg["messages"]["noperm_log"])
    
    # Remove administrators
    @admin.subcommand(description='Remove an administrator')
    async def rm(self, interaction: nextcord.Interaction, user: Optional[nextcord.Member] = nextcord.SlashOption(description='Who to revoke administrative privileges from',
            required=True), mention_user: Optional[bool] = nextcord.SlashOption(
            description='Whether or not to ping the former admin in the resulting message', required=False, default=False, choices={'Yes':True, 'No':False})):
        db = Database(interaction.guild, reason='Slash command `/admin rm`')
        if interaction.user.id == interaction.guild.owner_id or interaction.user.id in db.fetch('admins')  or interaction.user.guild_permissions.administrator:
            admins = db.fetch('admins')
            if mention_user:
                show_user = user.mention
            else:
                show_user = user.name
            try:
                if user.id in admins:
                    db.set('admin', user.id, clear=True)
                    await interaction.send(f'Removed {show_user} from admins.')
                else:
                    await interaction.send(f'User {user.name} is not an admin.')
            except Exception as ex:
                await interaction.send(self.cfg['messages']['error'].replace('[[error]]', str(ex)))
                logger.exception(f'{ex}')
            db.close()
        else:
            await interaction.send(self.cfg["messages"]["noperm"], ephemeral=True)
            logger.debug(self.cfg["messages"]["noperm_log"])

def setup(bot):
    bot.add_cog(Admin(bot))
    logger.debug('Setup cog "admin"')