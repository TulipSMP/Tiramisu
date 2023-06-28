# 
# Tiramisu Discord Bot
# --------------------
# Nextcord Tasks
# 
from logging42 import logger
import nextcord
from nextcord.ext import commands
import yaml
from libs.database import Database
from libs import levelling

class Tasks(commands.Cog):
    """ This cog is for tasks that must be run on various bot events """
    def __init__(self, bot):
        self.bot = bot
        self.client = nextcord.Client()

    client = nextcord.Client()

    # Events
    @commands.Cog.listener('on_ready')
    async def on_ready(self):
        logger.info('Loaded cog tasks.py')
        # Ensure databases exist for each guild the bot is in
        guilds = await self.bot.fetch_guilds(limit=None).flatten()
        logger.info(f'Verifying Database. Guilds: {guilds}')
        for guild in guilds:
            db = Database(guild, reason = f'Verifying database for guild {guild.id} (on start).')
            db.verify()
            db.close()

            levelling.setup(guild)

        # Show the cool welcome messages
        with open('config/welcomescreen.yml', 'r') as ymlfile:
            welcomescreen = yaml.load(ymlfile, Loader=yaml.FullLoader)

        for line in welcomescreen['message']:
            logger.info(line)

    
    @commands.Cog.listener('on_guild_join')
    async def on_guild_join(self, guild):
        # Create databases on joining a guild
        logger.info(f'Creating database tables for newly joined guild {guild.id}')
        db = Database(guild, reason = f'Creating database for new guild {guild.id}')
        db.create()
        db.verify()
        # Set admin and DM them
        db.set('admin', guild.owner_id)
        await guild.owner.send(f'''Thanks for adding me to your server! Use the `/admin` commands to add other administrators, \
and use the `/setting` commands to change settings for the bot.\nTo learn more about how to use {self.bot.user.name}, try the `/help` command.''')
        db.close()
        levelling.setup(guild)

    @commands.Cog.listener('on_guild_remove')
    async def on_guild_remove(self, guild):
        logger.info(f'Removing tables for guild {guild.id} on leave!')
        db = Database(guild, reason = f'Deletion upon guild leave')
        db.delete()
        db.close()
        logger.success(f'Removed tables for removed guild {guild.id}!')

    @commands.Cog.listener()
    async def on_member_join(self, member: nextcord.Member):
        db = Database(member.guild, reason='Tasks, check `system_channel`')
        try:
            channel = member.guild.get_channel(int(db.fetch('system_channel')))
            if channel == None:
                raise ValueError
        except ValueError:
            return
        
        await channel.send(f'**Welcome {member.mention} to the server!**')
    
    @commands.Cog.listener()
    async def on_member_remove(self, member: nextcord.Member):
        db = Database(member.guild, reason='Tasks, check `system_channel`')
        try:
            channel = member.guild.get_channel(int(db.fetch('system_channel')))
            if channel == None:
                raise ValueError
        except ValueError:
            return
        
        await channel.send(f'**Goodbye {member.display_name}**')
        
def setup(bot):
    bot.add_cog(Tasks(bot))
    logger.debug('Setup cog "tasks"')