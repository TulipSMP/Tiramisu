from logging42 import logger
import nextcord
from nextcord.ext import commands
import yaml
import mysql.connector

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Load Yaml
    with open("config/config.yml", "r") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
    logger.info(f'CONFIG.yml:\n{cfg}')
    
    # Test guild ID
    TESTING_GUILD_ID=cfg["discord"]["testing_guild"]

    # Database
    logger.debug("Logging into DB from admin.py")
    import mysql.connector
    sql = mysql.connector.connect(
        host=cfg["mysql"]["host"],
        user=cfg["mysql"]["user"],
        password=cfg["mysql"]["pass"],
        database=cfg["mysql"]["db"]
    )

    # Load bot owner from yaml
    botowner = cfg["discord"]["owner"]

    # Load Admins from DB
    cursor = sql.cursor()
    cursor.execute('SELECT id FROM admins;')
    admins = cursor.fetchall()
    #admins = []
    #for admin_id in admins_raw:
    #    admin_new = admin_id.replace(',', '', 1)
    #    admins.append(admin_new)

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        logger.info('Loaded cog admin.py')

    # Commands
    @nextcord.slash_command(guild_ids=[TESTING_GUILD_ID])
    async def admin(self, interaction: nextcord.Interaction):
        pass
        # This command is to set up the following as subcommands
    
    # Add an instance administrator
    @admin.subcommand(description="Add an administrator")
    async def add(self, interaction: nextcord.Interaction, user: nextcord.Member):
        if interaction.user.id == self.botowner:
            cursor = self.sql.cursor()
            try:
                cursor.execute(f"INSERT INTO admins (id, permission) VALUES ('{user.id}', 1);")
                await interaction.send(f"Added {user.mention} as an admin.")
                logger.debug(f'{interaction.user.name} added {user.name} as bot administrator')
            except Exception as ex:
                await interaction.send(f'**An Error occured:**\n```\n{ex}\n```\nPlease contact the devs.')
                logger.exception(f'{ex}')
        else:
            await interaction.send(cfg["messages"]["noperm"], ephemeral=True)
    
    # List administrators
    @admin.subcommand(description='List administrators')
    async def list(self, interaction: nextcord.Interaction):
        if interaction.user.id == self.botowner or interaction.user.id in self.admins:
            msg = f'**Registered Administrators:**\n'
            for id in self.admins:
                msg += f'• {id}\n'
            await interaction.send(msg)
            logger.debug(f"Listed administrators {self.admins} for {interaction.user.name} ({interaction.user.id})")
        else:
            await interaction.send(self.cfg["messages"]["noperm"], ephemeral=True)
            logger.debug(self.cfg["messages"]["noperm_log"])
    
    # Remove administrators
    @admin.subcommand(description='Remove an administrator')
    async def rm(self, interaction: nextcord.Interaction, user: nextcord.Member, mention_user=True):
        if interaction.user.id == self.botowner or interaction.user.id in self.admins:
            cursor = self.sql.cursor()
            if mention_user:
                show_user = user.mention
            else:
                show_user = user.name
            try:
                if user.id in self.admins:
                    cursor.execute(f'DELETE FROM TABLE WHERE id IS {user.id}')
                    await interaction.send(f'Removed {show_user} from admins.')
                else:
                    await interaction.send
            except Exception as ex:
                await interaction.send(f'**An Error occured:**\n```\n{ex}\n```\nPlease contact the devs.')
                logger.exception(f'{ex}')
        else:
            await interaction.send(self.cfg["messages"]["noperm"], ephemeral=True)
            logger.debug(self.cfg["messages"]["noperm_log"])

def setup(bot):
    bot.add_cog(Admin(bot))
    logger.debug('Setup cog "admin"')