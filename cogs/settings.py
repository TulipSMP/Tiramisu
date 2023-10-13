# 
# Tiramisu Discord Bot
# --------------------
# Guild Settings Commands
# 
from logging42 import logger

import nextcord
import yaml

from nextcord.ext import commands
from typing import Optional

from libs.database import Database
from libs import utility, extensions


class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open('config/settings.yml', 'r') as settings_yml:
            self.settings = yaml.load(settings_yml, Loader=yaml.FullLoader)
    
    # Fetch yaml values for use in function definitions
    with open("config/config.yml", "r") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

    with open("config/settings.yml", "r") as settings_yml:
        settings_raw = yaml.load(settings_yml, Loader=yaml.FullLoader)
        SETTINGS = settings_raw['settings'] + extensions.get_all_shown_settings()

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        logger.info('Loaded cog settings.py')

    # Commands
    @nextcord.slash_command(description='Change and view settings')
    async def setting(self, interaction: nextcord.Interaction):
        pass

    @setting.subcommand(description='View settings')
    async def get(self, interaction: nextcord.Interaction, 
        setting: Optional[str] = nextcord.SlashOption(description='Which setting to view. Use "all" to get a list of available options.', required=True, )): #choices=SETTINGS + ['all'])):
        db = Database(interaction.guild, reason='Slash command `/setting get`')
        if interaction.user.id in db.fetch('admins'):
            if setting in self.settings['settings'] + extensions.get_all_shown_settings():
                value = db.fetch(setting)
                try:
                    if self.bot.get_channel(int(value)) != None:
                        value_channel = self.bot.get_channel(int(value))
                        value = value_channel.mention
                    elif interaction.guild.get_role(int(value)) != None:
                        value_role = interaction.guild.get_role(int(value))
                        value = value_role.mention
                    elif self.bot.get_user(int(value)) != None:
                        value_user = self.bot.get_user(int(value))
                        value = value_user.mention
                except TypeError:
                    pass
                except ValueError:
                    pass
                message = f'Setting **{setting}** is currently set to __{value}__'
            elif setting == 'all':
                message = f'**Available settings:**\n'
                for entry in self.settings['settings'] + extensions.get_all_shown_settings():
                    message += f'• `{entry}`\n'
            else:
                message = 'No such setting. Use `all` to get a list of all available settings'
            await interaction.send(message)
        else:
            await interaction.send(self.cfg['messages']['noperm'], ephemeral=True)
    
    @setting.subcommand(description='Change settings')
    async def set(self, interaction: nextcord.Interaction,
        setting: Optional[str] = nextcord.SlashOption(description='Which setting to change', required=True, ), #choices=SETTINGS),
        value: Optional[str] = nextcord.SlashOption(description='What to change it to', default='none')):
        db = Database(interaction.guild, reason='Slash command `/setting set`')
        if interaction.user.id in db.fetch('admins'):
            setting = setting.strip()
            if setting not in self.settings['settings']:
                valid = False
                response = 'That is not a valid setting. Use `/setting get:all` to see all available settings.'
            else:
                valid, new_value, response = utility.valid_setting(interaction.guild, setting, value)

            if valid:
                db.set(setting, new_value)
                db.close()
                message = f'**Setting Changed**\n`{setting}` is now set to __{value}__!'
            else:
                message = f'Could not change setting!\n*{response}*'
            
            await interaction.send(message)
        else:
            await interaction.send(self.cfg['messages']['noperm'], ephemeral=True)
    
def setup(bot):
    bot.add_cog(Settings(bot))
    logger.debug('Setup cog "settings"')
