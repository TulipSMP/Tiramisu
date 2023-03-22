from logging42 import logger
import nextcord
from nextcord.ext import commands
import yaml
from libs.database import Database

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.client = bot
    

    # Variables
    with open("config/config.yml", "r") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
    TESTING_GUILD_ID=cfg["discord"]["testing_guild"]

    # Error Function
    def error(self, error):
        logger.error(f"Error in moderation.py: {error}")
        return cfg['messages']['error'].replace('[[error]]', error)

    # No Permission Function
    def noperm(self, cmd, interaction):
        logger.debug(cfg['messages']['noperm_log'].replace('[[user]]', interaction.user.name).replace('[[user_id]]', interaction.user.id).replace('[[command]]', cmd))
        return cfg['messages']['noperm']

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        logger.info('Loaded cog moderation.py!')

    # Commands
    @nextcord.slash_command(description="Warn a User", guild_ids=[TESTING_GUILD_ID])
    async def warn(self, interaction: nextcord.Interaction, user: nextcord.Member, reason='No reason given.',
        show_message='Whether to publicly display a warn in your current channel, in addition to a DM.'):
        """ Warn a User """
        db = Database(interaction.guild.id, reason=f'Check for permission, `/warn`')
        if interaction.user in db.fetch('admins'):
            try:
                await user.send(f"*You have been warned in __{interaction.guild.name}__! For:*\n> **{reason}**\n\
                    Please make sure you have read this server's rules.")
                logger.debug(f'{interaction.user.id} warned {user.id} for {reason}')
                await interaction.channel.send(f"{user.mention} has been warned for:\n{reason}", ephemeral=show_message)
                try:
                    modlog_channel = db.fetch('modlog_channel')
                    if modlog_channel != 'none' or modlog_channel != None:
                        log_channel = self.client.get_channel(modlog_channel)
                        await log_channel.send(f'{user.mention} was warned by {interaction.user.name}#{interaction.user.discriminator} ID: `{interaction.user.id}`')
                        logging_info = f'This action was logged successfully in {log_channel.mention}.'
                    else:
                        logging_info = f'Logging of moderation actions is not set up.'
                except:
                    logging_info = f'There was an error while trying to log this action.'
                await interaction.send(f'{user.mention} was successfully warned!\n*{logging_info}*')
            except BaseException as e:
                await interaction.send(error(e), ephemeral=True)
        else:
            await interaction.response.send(noperm('warn', interaction), ephemeral=True)
"""
    @nextcord.slash_command(description="Make an announcement!", guild_ids=[TESTING_GUILD_ID])
    async def announce(self, interaction: nextcord.Interaction, ping: bool, message: str):
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
            await interaction.response.send(noperm('announce', interaction), ephemeral=True)
"""
def setup(bot):
    bot.add_cog(Moderation(bot))
    logger.debug('Setup cog "moderation"')