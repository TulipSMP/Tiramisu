from logging42 import logger
import nextcord
from nextcord.ext import commands
import yaml
from libs.database import Database
from typing import Optional

class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open('config/settings.yml', 'r') as settings_yml:
            self.settings = yaml.load(settings_yml, Loader=yaml.FullLoader)
    
    # Fetch yaml values for use in function definitions
    with open("config/config.yml", "r") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
    TESTING_GUILD_ID=cfg["discord"]["testing_guild"]

    with open("config/settings.yml", "r") as settings_yml:
        settings_raw = yaml.load(settings_yml, Loader=yaml.FullLoader)
        SETTINGS = settings_raw['settings']

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        logger.info('Loaded cog settings.py')

    # Functions
    def occurs(self, string: str, char: str):
        count = 0
        for i in string:
            if i == char:
                count += 1
        return count

    # Commands
    @nextcord.slash_command(description='Change and view settings', guild_ids=[TESTING_GUILD_ID])
    async def setting(self, interaction: nextcord.Interaction):
        pass

    @setting.subcommand(description='View settings')
    async def get(self, interaction: nextcord.Interaction, 
        setting: Optional[str] = nextcord.SlashOption(description='Which setting to view. Use "all" to get a list of available options.', required=True, choices=SETTINGS + ['all'])):
        db = Database(interaction.guild, reason='Slash command `/setting get`')
        if interaction.user.id in db.fetch('admins'):
            if setting in self.settings['settings']:
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
                for entry in self.settings['settings']:
                    message += f'• `{entry}`\n'
            else:
                message = 'No such setting. Use `all` to get a list of all available settings'
            await interaction.send(message)
        else:
            await interaction.send(self.cfg['messages']['noperm'], ephemeral=True)
    
    @setting.subcommand(description='Change settings')
    async def set(self, interaction: nextcord.Interaction,
        setting: Optional[str] = nextcord.SlashOption(description='Which setting to change', required=True, choices=SETTINGS),
        value: Optional[str] = nextcord.SlashOption(description='What to change it to', default='none')):
        db = Database(interaction.guild, reason='Slash command `/setting set`')
        if interaction.user.id in db.fetch('admins'):
            if setting in self.settings['settings']:
                if value == 'none':
                    should_clear = True
                else:
                    should_clear = False
                
                if setting.endswith('_channel'):
                    value = value.strip(' <#>')
                    kind = 'channel'
                elif setting.endswith('_role'):
                    value = value.strip(' <@&>')
                    kind = 'role'
                elif setting.endswith('_user'):
                    value = value.strip(' <@>')
                    kind = 'user'
                elif setting.endswith('_address'):
                    kind = 'address'
                else:
                    kind = 'text'

                if db.set(setting, value, clear=should_clear):
                    try:
                        value = int(value)
                    except TypeError:
                        pass
                    except ValueError:
                        pass

                    channel = False
                    role = False
                    user = False
                    address = False

                    try:
                        if self.bot.get_channel(value) != None:
                            value_channel = self.bot.get_channel(int(value))
                            value = value_channel.mention
                            channel = True
                        elif interaction.guild.get_role(value) != None:
                            value_role = interaction.guild.get_role(int(value))
                            value = value_role.mention
                            role = True
                        elif self.bot.get_user(value) != None:
                            value_user = self.bot.get_user(int(value))
                            value = value_user.mention
                            user = True
                        elif self.occurs(value, '.') >= 2 and setting.endswith('_address'):
                            address = True
                    except TypeError:
                        pass
                    except ValueError:
                        pass
                    if should_clear:
                        message = f'Successfully set **{setting}** back to default.\nTo set it to a custom value, remember to use the `value:` option.'
                    else:
                        suffix = ''
                        if kind == 'channel' and not channel:
                            suffix = '\n**Warning:** This should be set to a valid channel!'
                        elif kind == 'role' and not role:
                            suffix = '\n**Warning:** This should be set to a valid role!'
                        elif kind == 'user' and not user:
                            suffix = '\n**Warning:** This should be set to a valid user!'
                        elif kind == 'address' and not address:
                            suffix = '\n**Warning:** This should be set to a valid address!'
                        message = f'Successfully set **{setting}** to __{value}__{suffix}'
                    logger.success(f'Changed setting "{setting}" for guild {db.guild.id}!')
                else:
                    message = f'Failed to set **{setting}**!'
                await interaction.send(message)
            else:
                message = f'No such setting. Use `/setting get setting:all` to see available settings.'
            db.close()
        else:
            await interaction.send(self.cfg['messages']['noperm'], ephemeral=True)
    
def setup(bot):
    bot.add_cog(Settings(bot))
    logger.debug('Setup cog "settings"')