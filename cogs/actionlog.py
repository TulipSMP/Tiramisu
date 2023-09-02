# 
# Tiramisu Discord Bot
# --------------------
# Log Actions not performed
# Via Tiramisu in the Modlog
# 
from logging42 import logger

import nextcord
from nextcord.ext import commands

import yaml

from libs.database import Database
from libs import utility, moderation

class ActionLog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        with open("config/config.yml", "r") as ymlfile:
            self.cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        logger.info('Loaded cog actionlog.py')

    @commands.Cog.listener()
    async def on_guild_audit_log_entry_create(self, entry: nextcord.AuditLogEntry):
        try:
            guild = entry.user.guild
            if guild == None:
                raise AttributeError
        except AttributeError:
            return

        asterisk = '*Not performed via Tiramisu*'
        match type(entry.action):
            case nextcord.AuditLogAction.kick:
                moderation.modlog(
                    guild,
                    f'👟 User Kicked *',
                    entry.user,
                    entry.target,
                    additional = {'*': asterisk},
                    reason = entry.reason,
                    action = 'kick'
                )
            case nextcord.AuditLogAction.ban:
                moderation.modlog(
                    guild,
                    f'🚷 User Banned*',
                    entry.user,
                    entry.target,
                    additional = {'*': asterisk},
                    reason = entry.reason,
                    action = 'kick'
                )
            case nextcord.AuditLogAction.unban:
                moderation.modlog(
                    guild,
                    f'🔨 User Unbanned*',
                    entry.user,
                    entry.target,
                    additional = {'*': asterisk},
                    reason = entry.reason,
                    action = 'unban'
                )
            # TODO: Action when user timed out.
            case other:
                pass


def setup(bot):
    bot.add_cog(ActionLog(bot))
    logger.debug('Setup cog "actionlog"')