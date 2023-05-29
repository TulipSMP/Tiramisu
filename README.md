# Tiramisu
##### Code Status: Active Development! Breaking changes and unstability may be present this branch.

An open source discord bot for all audiences, developed by the folks at RoseSMP.

### ⚠️ Not Ready for Production
This bot is not finished, and is far from useable. In the meantime, feel free to open a pull request to help us out.

## Getting Started
See [Getting Started](./doc/getting-started.md) for instructions on how to run and develop this bot.

All our documentation is in the [doc/](/doc/) directory.

## Roadmap
There's a lot of things we'd like to do with this bot, but here's a general idea of our current scope of the project

### Commands
#### For Moderation
- [x] `/warn` (with dm) [user, reason]
- [x] `/announce` [pings bool, message]
- [x] `/addrole` give all users a specific role (and `/delrole`)
- [x] `/kick` kick a user from the server

#### For Users
- [ ] `/help`: sends DM to user about available commands
- [x] `/ip`: sends server IP address and join info (for game servers)
- [x]  `/report `
  * [x] Report Players and Users
  * [x] Report vulnerabilities/bugs
- [ ] Ticketing system
  1. Simple command or button to create ticket
  1. ticket categories 
- [ ] Mod application system
  * Question 'modules'
    - multiple choice
    - yes/no
    - free answer
  * Configurable per guild
  * Different position applications (guild configurable)

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
- [x] Get role and guild IDs from db
- [x] Guild-specific settings system via db
