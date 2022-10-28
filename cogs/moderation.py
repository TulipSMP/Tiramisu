import nextcord
from nextcord.ext import commands


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.client = bot
    
    # Variables
    error_msg=f'⚠️ **An Error Occured!**\n```\n{e}\n```\nPlease report this to the devs.'
    staff = 1035378549403684864
    TESTING_GUILD_ID=1035313572638638110
    noperm = f'No permission!'

    # Channel & Role IDs
    ANNOUNCEMENT_CHANNEL=0000000000000000000
    ANNOUNCEMENT_ROLE=0000000000000000000

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print('Cog moderation.py loaded!')

    # Commands
    @commands.command(description="Warn a User", guild_ids=[TESTING_GUILD_ID])
    async def warn(interaction: nextcord.Interaction, arg: nextcord.Member, reason=str):
        if interaction.user.get_role(staff):
            if reason is None:
                reason = "No reason given."
            try:
                await arg.send(f"**You have been warned!**\nReason: __{reason}__\nPlease do not do this again. Make sure you have read the server rules.")
                await interaction.send(f"{arg.mention} has been warned for:\n{reason}")
            except BaseException as e:
                await interaction.send(error_msg)
                print(error_msg)
        else:
            await interaction.response.send(noperm, ephemeral=True)

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
                await interaction.send(error_msg)
                print(error_msg)
        else:
            await interaction.response.send(noperm, ephemeral=True)

def setup(bot):
    bot.add_cog(Moderation(bot))