from logging42 import logger
import nextcord
from nextcord.ext import commands
import yaml
from libs.database import Database
from typing import Optional

class Announce(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    with open("config/config.yml", "r") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
    TESTING_GUILD_ID=cfg["discord"]["testing_guild"]

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        logger.info('Loaded cog announce.py')

    # Commands
    @nextcord.slash_command(description="Make an announcement", guild_ids=[TESTING_GUILD_ID])
    async def announce(self, interaction: nextcord.Interaction, 
        announcement: Optional[str] = nextcord.SlashOption(required=True, description='What to say in the announcement'),
        ping: Optional[bool] = nextcord.SlashOption(required=False, description='Should your announcement role be pinged?')):
        db = Database(interaction.guild, reason = 'Slash command `/announce`')
        if interaction.user.id in db.fetch('admins'):
            channel = db.fetch('announcement_channel')
            role = db.fetch('announcement_role')
            logger.success(f'[DEBUG MESSAGE] Announcement channel: {role}')
            if channel == 'none':
                await interaction.send('The announcement channel is not set!\n\
Set it by copying the ID of the channel, and using the command `/setting set setting:announcement_channel`.')
            elif role == 'none' and ping == True:
                await interaction.send('The announcement role is not set!\n\
Set it by copying the ID of the role, and using the command `/setting set setting:announcement_role`.')
            else:
                try:
                    channel_obj = self.bot.get_channel(int(channel))
                except ValueError:
                    channel_obj = None
                try:
                    role_obj = interaction.guild.get_role(int(role))
                    logger.success(f'Role object is: {role_obj}')
                except ValueError:
                    role_obj = None
                if channel_obj == None:
                    await interaction.send('The announcement channel is not set to an acceptable value!\n\
Set it by copying the ID of the channel, and using the command `/setting set setting:announcement_channel`.')
                    return
                if role_obj == None and ping == True:
                    await interaction.send('The announcement role is not set to an acceptable value!\n\
Set it by copying the ID of the role, and using the command `/setting set setting:announcement_role`.')
                    return
                announcement = announcement.replace('\\n', '\n')
                if ping:
                    await channel_obj.send(f'**Announcement!** ||{role_obj.mention}||\n>>> {announcement}\n       *Announced By: {interaction.user.display_name}*')
                else:
                    await channel_obj.send(f'**Announcement!** \n> {announcement}\n*Announced By: {interaction.user.display_name}*')
                await interaction.send(f'Announcement sent! See {channel_obj.mention}')
        else:
            await interaction.send(self.cfg['messages']['noperm'], ephemeral=True)

def setup(bot):
    bot.add_cog(Announce(bot))
    logger.debug('Setup cog "announce"')