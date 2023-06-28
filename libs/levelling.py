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

def delete(guild: nextcord.Guild):
    """ Delete `guild`'s levelling tables """
    db = Database(guild, reason='Levelling, delete table')
    db.raw(f'DROP TABLE "levels_{db.guild.id}");', fetchall=False, fetchone=False)
    db.close()

def get_points(member: nextcord.Member):
    """ Get a member's point count """
    db = Database(member.guild, reason='Levelling, get points')
    
    try:
        (result, *x) = db.raw(f'SELECT points FROM "levels_{db.guild.id}" WHERE id={member.id};', fetchone=True, fetchall=False)
        return int(result)
    except ValueError:
        return 0
    except TypeError:
        return 0

def get_level(member: nextcord.Member, cached_pts: int = None):
    """ Get a member's level """
    
    if cached_pts != None:
        points = cached_pts
    else:
        points = get_points(member)

    if points <= 0:
        return 0

    level_raw = math.log2(points/10)

    level_current = int(math.trunc(level_raw))

    if level_current < 0:
        level_current = 0

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


def reset_points(member: nextcord.Member):
    """ Reset `member`'s points """
    db = Database(member.guild, reason='Levelling, reset points')

    db.raw(f'DELETE FROM "levels_{db.guild.id}" WHERE id={member.id};')

    db.close()

def get_leaderboard(guild: nextcord.Guild) -> dict:
    """ Get dictionary of user IDs and points, sorted by highest points. """
    db = Database(guild, reason='Levelling, get leaderboard')

    top = db.raw(f'SELECT * FROM "levels_{db.guild.id}" ORDER BY id LIMIT 5 ;', fetchall=True)

    top_dict = {}
    for user, points in top:
        top_dict[user] = points
    
    return top_dict
