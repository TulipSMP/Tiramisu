# Rosebot v3
The Rosebot Discord bot written using Nextcord

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
  1. Options: User reported (optional), in mc or discord, rule #, notes (optional)
  1. Hidden message 
  1. Create private channel (in reports category) visible by staff and reporter
  1. Message in #mod-chat or another channel abt report, linking to the new channel
  1. non-slash command (like `!close`) that DMs the user their report ticket was closed, makes the channel read-only, and hides it from the ticketer.
   

### Other Features
#### Bot Management
- [x] Cogs
  - [x] Load Cogs
  - [x] Unload Cogs
  - [x] Reload Cogs
- [ ] Shutdown bot correctly (instead of just an exit)

#### Messages & Variables
- [ ] Load ALL reused messages from yaml
- [ ] Get bot token from yaml or db
- [ ] Get role and guild IDs from yaml or db