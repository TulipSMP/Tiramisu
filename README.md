# Tiramisu
An open source discord bot for all audiences, developed by the folks at RoseSMP.

### ⚠️ Not Ready for Production
This bot is not finished, and is far from useable. In the meantime, feel free to open a pull request to help us out.

## Getting Started
See [Getting Started](./doc/getting-started.md) for instructions on how to run and develop this bot.

## Roadmap
There's a lot of things we'd like to do with this bot, but here's a general idea of our current scope of the project

### Commands
#### For Moderation
- [ ] `/warn` (with dm) [user, reason]
- [ ] `/announce` [pings bool, message]
- [ ] `/addrole` give all users a specific role

#### For Users
- [ ] `/help`: sends DM to user about available commands
- [ ] `/ip`: sends server IP address (for minecraft servers)
- [ ]  `/report `
  * [ ] Report Players
    1. Options: User reported (optional), in mc or discord, rule #, notes (optional)
    1. Hidden message 
    1. Create private channel (in reports category) visible by staff and reporter
    1. Message in #mod-chat or another channel abt report, linking to the new channel
    1. command that DMs the user their report ticket was closed, makes the channel read-only, and hides it from the ticketer.
  * [ ] Report vulnerabilities/bugs
    1. Options: where, when, what
    1. reward for players reporting
    1. listed in private channel just for mods/admins
- [ ] Ticketing system
  1. Simple command or button to create ticket
  1. ticket categories 

### Other Features
#### Bot Management
- [x] Cogs
  - [x] Load Cogs
  - [x] Unload Cogs
  - [x] Reload Cogs
- [x] Shutdown bot correctly (instead of just an exit)

#### Messages & Variables
- [x] Load most reused messages from yaml
- [x] Get bot token from yaml
- [ ] Get role and guild IDs from db
- [ ] Server-specific settings system via db
