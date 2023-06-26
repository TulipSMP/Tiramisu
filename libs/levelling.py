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
    db.close()

def get_points(member: nextcord.Member):
    """ Get a member's point count """
    db = Database(member.guild, reason='Levelling, get points')
    
    try:
        (result, *x) = db.raw(f'SELECT points FROM "levels_{db.guild.id}" WHERE id={member.id};', fetchone=True, fetchall=False, suppress_errors=True)
        return int(result)
    except ValueError:
        return 0
    except TypeError:
        return 0

def get_level(member: nextcord.Member):
    """ Get a member's level """
    
    points = get_points(member)

    if points <= 0:
        return 0

    level_raw = math.log(points)

    level_current = int(math.trunc(level_raw))

    return level_current

def add_points(member: nextcord.Member, points: int):
    """ Add `points` to `member` """
    db = Database(member.guild, reason='Levelling, add points')

    current = get_points(member)

    if current == 0:
        db.raw(f'INSERT INTO "levels_{db.guild.id}" (id, points) VALUES ({member.id}, {points});')
    else:
        db.raw(f'UPDATE "levels_{db.guild.id}" SET points={current + points} WHERE id={member.id}')
    
    db.close()