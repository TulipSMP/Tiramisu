from logging42 import logger
import nextcord
from nextcord.ext import commands
import yaml

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.client = bot
    
    # Error Function
    def error(error):
        logger.error(f"Error in moderation.py: {error}")
        return f'⚠️ **An Error Occured!**\n```\n{error}\n```\nPlease report this to the devs.'

    # No Permission Function
    def noperm(cmd):
        logger.debug(f'{interaction.user.name} (ID: {interaction.user.id}) \
            tried to run "{cmd}" but doesnt have permission!')
        return 'No Permission!'

    # Variables
    with open("config/config.yml", "r") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
    TESTING_GUILD_ID=cfg["discord"]["testing_guild"]

    staff = cfg["discord"]["roles"]["staff"]

    # Channel & Role IDs
    ANNOUNCEMENT_CHANNEL=0000000000000000000
    ANNOUNCEMENT_ROLE=0000000000000000000

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        logger.info('Cog moderation.py loaded!')

    # Commands
    @commands.command(description="Warn a User", guild_ids=[TESTING_GUILD_ID])
    async def warn(interaction: nextcord.Interaction, arg: nextcord.Member, reason=str):
        if interaction.user.get_role(staff):
            if reason is None:
                reason = "No reason given."
            try:
                await arg.send(f"**You have been warned!**\nReason: __{reason}__\n\
                    Please do not do this again. Make sure you have read the server rules.")
                await interaction.send(f"{arg.mention} has been warned for:\n{reason}")
                logger.debug(f'{interaction.user} warned {arg.display_name} for {reason}')
            except BaseException as e:
                await interaction.send(error(e), ephemeral=True)
        else:
            await interaction.response.send(noperm('announce'), ephemeral=True)

    @commands.command(description="Make an announcement!", guild_ids=[TESTING_GUILD_ID])
    async def announce(interaction: nextcord.Interaction, ping: bool, message: str):
        if interaction.user.get_role(staff):
            try:
                if ping:
                    prepend = f'<@{ANNOUNCEMENT_ROLE}>:\n'
                else:
                    prepend = 'Announcement:'
                channel = client.get_channel(ANNOUNCEMENT_CHANNEL)
                await channel.send(f"{prepend}> {message}\n*Announced by <@{interaction.user.id}>.*")
                await interaction.send(f"Announcement sent! See <#{ANNOUNCEMENT_CHANNEL}>")
            except BaseException as e:
                await interaction.send(error(e), ephemeral=True)
        else:
            await interaction.response.send(noperm('announce'), ephemeral=True)

def setup(bot):
    bot.add_cog(Moderation(bot))
    logger.debug('Setup cog "moderation"')