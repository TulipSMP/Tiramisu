from logging42 import logger
import nextcord
from nextcord.ext import commands
import yaml
import mysql.connector
import sqlite3
from libs.database import Database

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Load Yaml
        with open("config/config.yml", "r") as ymlfile:
            cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
        self.cfg = cfg
    
    with open("config/config.yml", "r") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
    # Test guild ID
    TESTING_GUILD_ID=cfg["discord"]["testing_guild"]

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        logger.info('Loaded cog admin.py')

    # Commands
    @nextcord.slash_command(guild_ids=[TESTING_GUILD_ID])
    async def admin(self, interaction: nextcord.Interaction):
        pass
        # This command is to set up the following as subcommands
    
    # Add a guild administrator
    @admin.subcommand(description="Add an administrator")
    async def add(self, interaction: nextcord.Interaction, user: nextcord.Member):
        if interaction.user.id == interaction.guild.owner_id or interaction.user.id in admins:
            db = Database(interaction.guild, reason='Slash command: `admin add`')
            admins = db.fetch(interaction.user.id, admin=True, return_list=True)
            #try:
            if user.id in admins:
                await interaction.send(f'`{user.name}#{user.discriminator}` is already an admin! ||(Their ID is `{user.id}`)||')
            else:
                if db.set('admin', user.id):
                    logger.debug(f'{interaction.user.name} added {user.name} as bot administrator')
                    await interaction.send(f"Added {user.mention} as an admin.")
            #except Exception as ex:
            #    await interaction.send(self.cfg['messages']['error'].replace('[[error]]', str(ex)))
            #    logger.exception(f'{ex}')
            db.close()
        else:
            await interaction.send(self.cfg["messages"]["noperm"], ephemeral=True)
    
    # List administrators
    @admin.subcommand(description='List administrators')
    async def list(self, interaction: nextcord.Interaction):
        if interaction.user.id == interaction.guild.owner_id or interaction.user.id in admins:
            db = Database(interaction.guild, reason='Slash command: `admin list`')
            msg = f'**Registered Administrators:**\n'
            try:
                msg_admins = str(db.fetch(interaction.user.id, admin=True, return_list=True))
                logger.info('ADMINS TABLE:' + msg_admins)
                #for id in admins:
                #    #usr = self.bot.get_user(id)
                #    #name = usr.name
                #    #msg_admins += f'• {name} `{id}`\n'
                #    msg_admins += f'• `{id}`\n'
                if msg_admins == '':
                    msg = '**No Registered Administrators.**'
                logger.debug(f"Listed administrators for {interaction.user.name} ({interaction.user.id})")
                await interaction.send(msg)
            except BaseException as ex:
                await interaction.send(self.cfg['messages']['error'].replace('[[error]]', str(ex)))
                logger.error(f'Failed to fetch list of admins for guild {db.guild.id}! Error: {ex}', exc_info=True)
            except sqlite3.OperationalError:
                await interaction.send(self.cfg['messages']['error'])
            db.close()
        else:
            await interaction.send(self.cfg["messages"]["noperm"], ephemeral=True)
            logger.debug(self.cfg["messages"]["noperm_log"])
    
    # Remove administrators
    @admin.subcommand(description='Remove an administrator')
    async def rm(self, interaction: nextcord.Interaction, user: nextcord.Member, mention_user=True):
        if interaction.user.id == interaction.guild.owner_id or interaction.user.id in admins:
            db = Database(interaction.guild, reason='Slash command: `admin rm`')
            admins = db.fetch(interaction.user.id, admin=True, return_list=True)
            if mention_user:
                show_user = user.mention
            else:
                show_user = user.name
            try:
                if user.id in admins:
                    db.set('admin', user.id, clear=True)
                    await interaction.send(f'Removed {show_user} from admins.')
                else:
                    await interaction.send(f'User {user.name} (ID: {user.id}) is not an admin.')
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