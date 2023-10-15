# 
# Tiramisu Discord Bot
# --------------------
# Youtube Subscription
# 
from logging42 import logger

import yaml
import feedparser
import nextcord
import dateutil.parser
import datetime
import time

from typing import Optional, Union, List
from libs.database import Database

def validate_yt(id: str) -> Optional[str]:
    """ Convert YT channel ID into RSS feed URL. """
    try:
        url = f'https://www.youtube.com/feeds/videos.xml?channel_id={id}'
        result = feedparser.parse(url)
        if result['bozo'] != False:
            return None
        return url
    except:
        return None

# Create + validate tables for a guild
# user int | feed str | checked int
# (discord user id) | (rss feel url) | (last checked timestamp)
def setup_tables(guild: nextcord.Guild) -> None:
    """ Setup Content Creator database tables for a guild """
    db = Database(guild, reason='YouTube, setup table')
    db.raw(f'CREATE TABLE IF NOT EXISTS "creators_{db.guild.id}" (user int, feed str, checked bigint);', fetch=False)
    db.close()

def remove_tables(guild: nextcord.Guild) -> None:
    """ Remove table for a guild """
    db = Database(guild, reason='YouTube, DROP table')
    db.raw(f'DROP TABLE "creators_{db.guild.id}";', fetch=False)
    db.close()

# Set/remove table row
def update_creator(guild: nextcord.Guild, user: Union[nextcord.Member, nextcord.User], feed: str = 'none') -> None:
    """ Add a creator to the table if it is not already there """
    db = Database(guild, reason='YouTube, edit creator')
    if user.id in db.raw(f'SELECT user FROM "creators_{db.guild.id}";'):
        db.raw(f'UPDATE "creators_{db.guild.id}" SET feed=? WHERE user={user.id}', (feed), fetch=False)
    else:
        db.raw(f'INSERT INTO "creators_{db.guild.id}" (user, feed, checked) VALUES ( ? , ? , ? );', 
            ( user.id, feed, int(time.time()) ), fetch=False)
    db.close()

def get_feed_data(url: str) -> Optional[dict]:
    """ Simplifies feed data """
    raw = feedparser.parse(url)
    entries = []
    for entry in raw['entries']:
        entries.append(
            {
                'title': entry['title'],
                'author': entry['author'],
                'author_url': entry['author_detail']['href'],
                'url': entry['link'],
                'id': entry['yt_videoid'],
                'published': int(dateutil.parser.parse(entry['published']).timestamp()),
                'description': entry['summary'],
                'thumbnail': entry['media_thumbnail'][0]['url'],
            }
        )

    basic = {
        'name': raw['feed']['title'],
        'link': raw['feed']['link'],
        'entries': entries
    }
    return basic

# Check for new videos for a guild
async def check_for_new(guild: nextcord.Guild, override_checktime: Optional[int] = None, post: bool = True) -> Optional[List[dict]]:
    """ Check for new videos and return a list of them (as formatted by get_feed_data() ) """
    db = Database(guild, reason='YouTube, check for new posts')
    try:
        creator_channel = guild.get_channel(int(db.fetch('creator_channel')))
        if creator_channel == None:
            raise ValueError
    except ValueError:
        return # Channel is not set up.
    creators = db.raw(f'SELECT * FROM "creators_{db.guild.id}";')

    new_posts= [] 
    for creator in creators:
        #try:
        if override_checktime != None:
            last_check = override_checktime
        else:
            last_check = creator[2] # Timestamp of when last checked
        db.raw(f'UPDATE "creators_{db.guild.id}" SET checked={int(time.time())} WHERE user={creator[0]};', fetch=False) # Update timestamp
        content = get_feed_data(creator[1])
        for entry in content['entries']:
            if entry['published'] >= last_check:
                logger.debug('YouTube/new Content Creator Video found!')
                new_posts.append(entry)
        #except:
        #    continue # fail silently

    if post:
        try:
            ping = guild.get_role(int(db.fetch('creator_ping_role')))
        except ValueError:
            ping = None
        for item in new_posts:
            await post_video(creator_channel, item, None, ping)
    db.close()
    return new_posts


async def post_video(channel: nextcord.TextChannel, video: dict, creator: Optional[Union[nextcord.Member, nextcord.User]], 
    ping: Optional[nextcord.Role]):
    """ Announce video in channel """
    if creator != None:
        note = f' ({creator.mention})'
    else:
        note = ''
    if ping != None:
        mention = f'\n{ping.mention}'
    else:
        mention = ''
    desc = video['description'].split('\n')[0]
    msg = f"## [{video['title']}]({video['url']})\nby [{video['author']}](<{video['author_url']}>){note}{mention}\n>>>{desc}{mention}"

    await channel.send(msg)

