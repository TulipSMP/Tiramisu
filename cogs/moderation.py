from logging42 import logger
import nextcord
from nextcord.ext import commands
import yaml
from libs.database import Database
from typing import Optional

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.client = bot
        
        with open("config/config.yml", "r") as ymlfile:
            self.cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
    
    TESTING_GUILD_ID=cfg["discord"]["testing_guild"]

    # Error Function
    def error(self, error):
        logger.error(f"Error in moderation.py: {error}")
        return self.cfg['messages']['error'].replace('[[error]]', error)

    # No Permission Function
    def noperm(self, cmd, interaction):
        logger.debug(cfg['messages']['noperm_log'].replace('[[user]]', interaction.user.name).replace('[[user_id]]', interaction.user.id).replace('[[command]]', cmd))
        return self.cfg['messages']['noperm']

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        logger.info('Loaded cog moderation.py!')

    # Commands
    @nextcord.slash_command(description="Warn a User", guild_ids=[TESTING_GUILD_ID])
    async def warn(self, interaction: nextcord.Interaction, user: nextcord.Member, 
        reason: Optional[str] = nextcord.SlashOption(description='Why this user is being warned.', default='No reason given.', required=False),
        show_message: Optional[bool] = nextcord.SlashOption(description='If a warn message should be sent in your current channel, in addition to the warn.', default=True)):
        """ Warn a User """
        db = Database(interaction.guild, reason=f'Check for permission, `/warn`')
        if interaction.user_id in db.fetch('admins'):
            try:
                logger.debug(f'{interaction.user.id} warned {user.id} for {reason}')
                await user.send(f"*You have been warned in __{interaction.guild.name}__! For:*\n>>> **{reason}**")
                await interaction.channel.send(f"{user.mention} has been warned for:\n{reason}", ephemeral=show_message)
                try:
                    modlog_channel = self.client.get_channel( int(db.fetch('modlog_channel')) )
                    if modlog_channel != None:
                        await modlog_channel.send(f'{user.mention} was warned by {interaction.user.name}#{interaction.user.discriminator} ID: `{interaction.user.id}`')
                        logging_info = f'This action was logged successfully in {modlog_channel.mention}.'
                    else:
                        logging_info = f'This action could not be logged. Make sure the `modlog_channel` setting is correct.'
                except:
                    logging_info = f'This action could not be logged. Make sure the `modlog_channel` setting is correct.'
                await interaction.send(f'{user.mention} was successfully warned!\n*{logging_info}*')
            except BaseException as e:
                await interaction.send(self.error(e), ephemeral=True)
        else:
            await interaction.send(self.noperm('warn', interaction), ephemeral=True)

def setup(bot):
    bot.add_cog(Moderation(bot))
    logger.debug('Setup cog "moderation"')