# 
# Tiramisu Discord Bot
# --------------------
# Content Creators
# 
from logging42 import logger
import nextcord
from nextcord.ext import commands
import yaml
from typing import Optional

from libs.database import Database
from libs import youtube

class Creators(commands.Cog):
    def __init__(self, bot):
        """ Creators Cog """
        self.bot = bot    
        with open("config/config.yml", "r") as ymlfile:
            self.cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)


    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        logger.info('Loaded cog creators.py')

    # Commands
    @nextcord.slash_command(description="Commands for Content Creators")
    async def creator(self, interaction: nextcord.Interaction):
        pass # for subcommands

    @creator.subcommand(description="Set channel ID")
    async def channel(self, interaction: nextcord.Interaction, 
        id: Optional[str] = nextcord.SlashOption(description="Channel ID from youtube.com/channel/CHANNELID", required=False)):
        db = Database(interaction.guild, reason='Creators, check perms')
        try:
            creator_role = interaction.guild.get_role(int(db.fetch('creator_role')))
            if creator_role == None:
                raise ValueError
        except ValueError:
            await interaction.send('Content Creators are not yet set up.\n*Ask an administrator to set the `creator_role` and `creator_channel` settings (see `/help topic:Content Creators`)*',
                ephemeral=True)
            return
        
        if creator_role in interaction.user.roles:
            if id == None:
                youtube.update_creator(interaction.guild, interaction.user, 'none')
                await interaction.send('Removed channel from your account.')
                return

            feed = youtube.validate_yt(id)
            if feed == None:
                await interaction.send("Invalid Channel ID.\n*If you're signed into the account your channel is associated with, you can [copy the Channel ID here](<https://www.youtube.com/account_advanced>). If not, see [this support page](<https://support.google.com/youtube/answer/3250431>).*",
                    ephemeral=True)
                return
            else:
                youtube.update_creator(interaction.guild, interaction.user, feed)
                data = youtube.get_feed_data(feed)
                await interaction.send(f"Updated Channel to [{data['name']}](<{data['link']}>).")
        else:
            await interaction.send(self.cfg['messages']['noperm'], ephemeral=True)


def setup(bot):
    bot.add_cog(Creators(bot))
    logger.debug('Setup cog "creators"')