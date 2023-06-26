# 
# Tiramisu Discord Bot
# --------------------
# Levelling System
# 
import nextcord
import math

from libs.database import Database

def setup(guild: nextcord.Guild):
    """ Setup tables for Levels """
    db = Database(guild, reason='Levelling, setup table')
    db.raw(f'CREATE TABLE IF NOT EXISTS "levels_{db.guild.id}" (id int, points int);', fetchall=False, fetchone=False)

def get_points(member: nextcord.Member):
    """ Get a member's point count """
    db = Database(member.guild, reason='Levelling, get points')
    
    try:
        (result, *x) = db.raw(f'SELECT points FROM "levels_{db.guild.id}" WHERE id={member.id};', fetchone=True, fetchall=False)
        return int(result)
    except ValueError:
        return 0

def get_level(member: nextcord.Member):
    """ Get a member's level """
    
    points = get_points(member)

    level_raw = math.log(points)

    level_current = int(math.trunc(level_raw))

    return level_current

def add_points(member: nextcord.Member, points: int):
    """ Add `points` to `member` """
    db = Database(member.guild, reason='Levelling, add points')
    
