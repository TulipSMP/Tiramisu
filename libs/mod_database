# 
# Tiramisu Discord Bot
# --------------------
# Extra Functions for Modlog DB
# 
from logging42 import logger

import nextcord

from libs.database import Database
from libs import moderation

def setup(guild: nextcord.Guild):
    """ Setup tables for Modlog """
    db = Database(guild, reason=f'Modlog, setup table if it doesnt exist for {guild.id}')
    db.raw(f'CREATE TABLE IF NOT EXISTS "modlog_{db.guild.id}" (timestamp int, uuid string, action string, moderator string, recipient string, reason string, extra string);', fetchall=False, fetchone=False)
    db.close()

def log(db: Database, timestamp: int, uuid: str, action: str, moderator: str, recipient: str, reason: str, extra: str):
    """ Log action in DB 
        see table /docs/modlog.md for db column descriptions """
    db.raw(f'INSERT INTO "modlog_{db.guild.id}" (timestamp, uuid, action, moderator, recipient, reason, extra) VALUES ( ? , ? , ? , ? , ? , ? , ? );',
        (timestamp, uuid, action, moderator, recipient, reason, extra,), fetch=False)

def remove(guild: nextcord.Guild):
    """ Remove tables for Modlog """
    db = Database(guild, reason=f'Modlog, remove tables for {guild.id}')
    db.raw(f'DROP TABLE "modlog_{db.guild.id}";', fetch=False)
    db.close()