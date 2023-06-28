# Levelling System
Tiramisu has a levelling system to encourage your users to talk on your server. Note that this does not do any form of spam prevention. It is up to your automod rules and moderators to stop spam in your server.


## Points
When someone sends a message, they are randomly added between 1 and 3 points, Unless their message is sent in one of the channels listed in the `no_points_channels` setting.
## Levels
Levels are calculated with the following equation, rounded down:
```
level = log₂( points ÷ 10 )
```
When someone levels up, a message is sent in the channel they were talking in.

## Disabling Levelling
To disable levelling, set the `no_points_channels` setting to `all`.

## Resetting Levels
If a user has been spamming, or you want to reset their level for any reason, moderators can use the `/resetlevel` command to set a user's points and level back to zero. This is logged in the `modlog_channel`

## Other Slash Commands
*(These are both disabled if levels are disabled as per the "Disabling Levelling" section)*

- `/level`: Displays your level and points
- `/leveltop`: Displays the top 10 users' levels and points


## Library
The levelling system uses the `libs.levelling` internal library which provides the following functions:

### *def **setup(guild: nextcord.Guild)***
Setup tables for Levels

Creates the required tables if they do not exist. This is run in `cogs/tasks.py`, on_ready() and on_guild_join().

Parameters:
- `guild`: nextcord.Guild, the guild to set up tables for

### *def **delete(guild: nextcord.Guild)***
Delete `guild`'s levelling tables

Drops the tables created by ***setup()*** for `guild`.

Parameters:
- `guild`: the nextcord.Guild to drop tables for

### *def **get_points(member: nextcord.Member)***
Get a `member`'s point count

Parameters:
- `member`: nextcord.Member, whose points to check

Returns `int`, their points

### *def **get_level(member: nextcord.Member, cached_pts: int = None)***
Get a member's level (based on their points)

Calls ***get_points()*** unless `cached_pts` is specified.

Uses the following algorithm to calculate the level:
```python
level_raw = math.log2(points/10)
level_current = int(math.trunc(level_raw))
```
In mathematical terms, that's equivalent to:
```math
log₂( points ÷ 10 )
```
Rounded down.


Parameters: 
- `member`: the nextcord.Member to calculate levels for

Optional:
- `cached_pts`: int, the points to calculate the level off of.

Returns `int`, the current level


### *def **add_points(member: nextcord.Member, points: int)***
Add `points` to `member`

Parameters:
- `member`: nextcord.Member, the user to give points to
- `points`: the amount of points to add

### *def **reset_points(member: nextcord.Member)***
Reset `member`'s points

Parameters:
- `member`: nextcord.Member, whom to reset points for

### *def **get_leaderboard(guild: nextcord.Guild)***
Get dictionary of user IDs and points, sorted by highest points.

Parameters:
- `guild`: nextcord.Guild, guild to get leaderboard for