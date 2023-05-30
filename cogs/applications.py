from logging42 import logger
import nextcord
from nextcord.ext import commands
import yaml
from libs.database import Database
from typing import Optional

class Applications(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        with open("config/config.yml", "r") as ymlfile:
            self.cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
    

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        logger.info('Loaded cog applications.py')

    # Commands
    @nextcord.slash_command(description="Apply for a position")
    async def apply(self, interaction: nextcord.Interaction,
        age_group: Optional[str] = nextcord.SlashOption(description='What age group are you in?',
            required=True, choices=["13 - 14 years old", "15 - 17 years old", "18 - 20 years old", "21+ years old"]),
        reason: Optional[str] = nextcord.SlashOption(description='Why should you be chosen as a moderator?', required=True, min_length=15, max_length=800),
        experience: Optional[bool] = nextcord.SlashOption(description='Have you moderated a community before?', required=True, 
            choices={"Yes":True, "No":False}),
        position: Optional[str] = nextcord.SlashOption(description='What position are you applying for?', default=None, required=False, max_length=15),):
        db = Database(interaction.guild, reason = 'Slash command `/apply`')
        try:
            channel = interaction.guild.get_channel(int(db.fetch('application_channel'))) 
            if channel == None:
                raise ValueError
        except ValueError:
            await interaction.send(f'The admins of this server have not set up applications! Ask them to set the `application_channel` setting to a valid channel ID.')
            return
        message = f'**Mod Application Opened**\nBy: __{interaction.user.name}#{interaction.user.discriminator} `{interaction.user.id}`__'
        if position != None:
            message += f'\nPosition Applied for: __{position}__'
        message += f'\nAge Group: __{age_group}__'
        if experience:
            message += '\n*This user has moderation experience*'
        else:
            message += '\n*This user does not have moderation experience*'
        message += f'\nWhy should this user be chosen as a moderator?\n> {reason}'
        await channel.send(message)
        await interaction.send(f'Your application has been submitted!', ephemeral=True)
        logger.info('Successfully completed an application.')

def setup(bot):
    bot.add_cog(Applications(bot))
    logger.debug('Setup cog "applications"')