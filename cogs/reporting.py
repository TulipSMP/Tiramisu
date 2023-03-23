from logging42 import logger
import nextcord
from nextcord.ext import commands
import yaml
from libs.database import Database
from typing import Optional

class Reporting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    with open("config/config.yml", "r") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
    TESTING_GUILD_ID=cfg["discord"]["testing_guild"]

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        logger.info('Loaded cog reporting.py')

    # Commands
    @nextcord.slash_command(description="Report a user or problem", guild_ids=[TESTING_GUILD_ID])
    async def report(self, interaction: nextcord.Interaction):
        pass

    @report.subcommand(description='Report a discord user to the moderators')
    async def user(self, interaction: nextcord.Interaction, user: nextcord.Member,
        reason: Optional[str] = nextcord.SlashOption(description='Why are you reporting this user?', required=True),):
        db = Database(interaction.guild, reason='Slash command `/report user`')
        try:
            modlog_channel =  interaction.guild.get_channel(int(db.fetch('modlog_channel')))
            if modlog_channel == None:
                raise ValueError
            else:
                await modlog_channel.send(f'**User Reported:**\nBy: {interaction.user.name}#{interaction.user.discriminator} (`{interaction.user.id}`)\
\nReported User: {user.mention} ({user.name}#{user.discriminator}`{user.id}`)\nReason: {reason}')
                logger.info('Successfully completed a warn action.')
                await interaction.send(f'Successfully sent your report to the moderators! Thanks for speaking up.', ephemeral=True)
        except ValueError:
            await interaction.send('The moderators have not yet (or incorrectly) set up where to send reports!\nAsk them to set the `modlog_channel` setting to the ID of the channel where logs should be sent.', ephemeral=True)
    
    @report.subcommand(description='Report a minecraft player to the moderators')
    async def player(self, interaction: nextcord.Interaction, 
        player: Optional[str] = nextcord.SlashOption(description='The username of the player to report', required=True),
        reason: Optional[str] = nextcord.SlashOption(description='Why are you reporting this player?', required=True),):
        db = Database(interaction.guild, reason='Slash command `/report user`')
        try:
            modlog_channel =  interaction.guild.get_channel(int(db.fetch('modlog_channel')))
            if modlog_channel == None:
                raise ValueError
            else:
                await modlog_channel.send(f'**Minecraft Player Reported:**\nBy: {interaction.user.name}#{interaction.user.discriminator} (`{interaction.user.id}`)\
\nReported User: `{player}`)\nReason: {reason}')
                logger.info('Successfully completed a report player action.')
                await interaction.send(f'Successfully sent your report to the moderators! Thanks for speaking up.', ephemeral=True)
        except ValueError:
            await interaction.send('The moderators have not yet (or incorrectly) set up where to send reports!\nAsk them to set the `modlog_channel` setting to the ID of the channel where logs should be sent.', ephemeral=True)
    @report.subcommand(description='Report a minecraft player to the moderators')
    async def bug(self, interaction: nextcord.Interaction, 
        place: Optional[str] = nextcord.SlashOption(description='Where does this bug occur?', required=True),
        behavior: Optional[str] = nextcord.SlashOption(description='What happens when this bug occurs?', required=True),
        expected: Optional[str] = nextcord.SlashOption(description='What should happen instead of this bug?', required=True),
        reproduce: Optional[str] = nextcord.SlashOption(description='What do you have to do for this bug to happen?', required=True),
        extra: Optional[str] = nextcord.SlashOption(description='Other info that might be helpful to us in fixing this bug', required=False, default=None)):
        db = Database(interaction.guild, reason='Slash command `/report user`')
        try:
            bugreports_channel =  interaction.guild.get_channel(int(db.fetch('bugreports_channel')))
            if bugreports_channel == None:
                raise ValueError
            else:
                if extra != None:
                    extra_info = f'\n**Extra Information:** {extra}'
                else:
                    extra_info = ''
                await bugreports_channel.send(f'**Bug Report!** By: {interaction.user.mention})\
\n**Place:** {place}\n**Bug:** {behavior}\n**What should happen:** {expected}\n**How to Reproduce:** {reproduce}{extra_info}')
                logger.info('Successfully completed a bug report action.')
                await interaction.send(f'Successfully sent your bug report in {bugreports_channel.mention}!', ephemeral=True)
        except ValueError:
            await interaction.send('The moderators have not yet (or incorrectly) set up where to send reports!\nAsk them to set the `bugreports_channel` setting to the ID of the channel where bug reports should be sent.', ephemeral=True)
def setup(bot):
    bot.add_cog(Reporting(bot))
    logger.debug('Setup cog "reporting"')