# 
# Tiramisu Discord Bot
# --------------------
# Debugging Utilities
# 
from logging42 import logger
import nextcord
from nextcord.ext import commands
import yaml

from libs.database import Database
from libs import buttons, ticketing, levelling, youtube

class Debug(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.persistent_views_added = False
    
    with open("config/config.yml", "r") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
    TESTING_GUILD_ID=cfg["discord"]["testing_guild"]

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        logger.info('Loaded cog debug.py')

        if not self.persistent_views_added:
            self.bot.add_view(buttons.PersistentTextButton())
            self.persistent_views_added = True

    bot = commands.Bot()

    # Commands
    @nextcord.slash_command(description='Commands for Debugging', guild_ids=[TESTING_GUILD_ID])
    async def debug(self, interaction: nextcord.Interaction):
        pass

    @debug.subcommand(description="Print DB")
    async def db(self, interaction: nextcord.Interaction, settings=False):
        db = Database(interaction.guild, reason='Fetch for debugging')
        if settings:
            t_type = 'settings'
            table = db.raw(f'select * from "settings_{db.guild.id}";')
        else:
            t_type = 'admins'
            table = db.fetch('admins')
        if table == False:
            table = 'Failed to fetch from database! OperationalError!'
            logger.warning('Failed to fetch data from database!')
        else:
            logger.debug(f"Printing db contents for {interaction.user.name}.")
        if t_type == 'admins':
            await interaction.response.send_message(f"Found these values in table `{t_type}_{db.guild.id}`: ```\n{table} ```\nType: `{type(table)}`\
                \nAre you (`{interaction.user.id}`) in list?: `{interaction.user.id in table}`")
        else:
            await interaction.response.send_message(f"Sending data to log")
            logger.info(f'Found this data in "{t_type}_{db.guild.id}":\n{table}')
        db.close()
    
    @debug.subcommand(description='Show a list of all members')
    async def members(self, interaction: nextcord.Interaction):
        message = '**List Of all Members:**'
        for user in interaction.guild.humans:
            message += f'\n • {user.name}#{user.discriminator} ({user.display_name}) ID: `{user.id}`'
        await interaction.send(message)


    @debug.subcommand(description='Check if this is a ticket')
    async def is_ticket(self, interaction: nextcord.Interaction):
        result, reason = await ticketing.is_ticket(interaction.channel, debug=True)
        if result:
            await interaction.send('🗹 This is a ticket!')
        else:
            await interaction.send(f'🗷 This is not a ticket: {reason}')
    
    @debug.subcommand(description='Get creator of ticket')
    async def ticket_creator(self, interaction: nextcord.Interaction):
        if await ticketing.is_ticket(interaction.channel):
            creator = await ticketing.get_ticket_creator(interaction.channel)
            await interaction.send(f'Ticket created by {creator.mention}')
        else:
            await interaction.send(f'This isn\'t a ticket.')

    @debug.subcommand(description='Test buttons')
    async def button(self, interaction: nextcord.Interaction):
        await buttons.HelloButton().start(interaction=interaction)
    
    @debug.subcommand(description='Add points')
    async def add_points(self, interaction: nextcord.Interaction, points: int):
        levelling.add_points(interaction.user, points)
        await interaction.send(f'You now have {levelling.get_points(interaction.user)} points!')\
    
    @debug.subcommand(description='Get Leaderboard')
    async def leveltop_raw(self, interaction: nextcord.Interaction):
        x = levelling.get_leaderboard(interaction.guild)
        await interaction.send(f'**Leaderboard:**\n{x}')

    @debug.subcommand(description='Start persistent view')
    async def persist_butons(self, interaction: nextcord.Interaction):
        await interaction.send("Test the thingy idfk", view=buttons.PersistentTextButton())
    
    @debug.subcommand(description='Post last video from a content creator')
    async def repost_content(self, interaction: nextcord.Interaction):
        db = Database(interaction.guild, reason='Debug, repost_content')

        try:
            channel = interaction.guild.get_channel(int(db.fetch('creator_channel')))
            if channel == None:
                raise ValueError
        except ValueError:
            await interaction.send('*Failed to fetch `creator_channel` to post to.*')
            return
        
        feed = await youtube.check_for_new(interaction.guild, override_checktime=0, post=False)
        try:
            video = feed[0]
        except IndexError:
            await interaction.send('*No videos have been posted by content creators*')
            return
        await youtube.post_video(channel, video, None, None)
        await interaction.send(f'Posted to {channel.mention}')

def setup(bot):
    with open("config/config.yml", "r") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
    
    if cfg['debug']: # Only enable debug cog if in debug mode
        bot.add_cog(Debug(bot))
        logger.debug('Setup cog "debug"')
