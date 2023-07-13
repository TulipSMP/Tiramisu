# tasks.py
For running validations and jobs that need to run upoun certain points.

## Tasks
### `on_ready`
* Verify Database (calls `db.verify()` on each guild in the cache).
* Create levelling tables if they do not exist (calls `levelling.setup()` on each guild in the cache)

### `on_guild_join`
* Create Database for joined guild (calls `db.create()`)
* Create levelling tables (calls `levelling.setup()`)

### `on_guild_leave`
* Delete tables of a guild (calls `db.delete()`)