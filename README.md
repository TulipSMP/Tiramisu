<div align="center"><img src='src/tiramisu.png' alt='Tiramisu, an italian cake with coffee, chocolate, and creamy white icing. Drawn in a simplistic square ' width=200>
<h1> Tiramisu </h1>
<a href="https://github.com/RoseSMP/Tiramisu/actions/workflows/pylint.yml"><img src="https://github.com/RoseSMP/Tiramisu/actions/workflows/pylint.yml/badge.svg?branch=main&event=push" alt="Lint"></a>
</div>

##### Code Status: Active Development! New features and breaking changes may be present in this branch.

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
- [x] Right-click user or message to perform mod action
- [ ] Logging of the following actions:
  * [x] Message Deletion
  * [x] Message Edit
  * [x] VC Join/Leave
  * [x] VC Start/Stop streaming/camera


#### For Users
- [x] `/help`: informs user on how to use the bot.
- [x] `/ip`: sends server IP address and join info (for game servers)
- [x]  `/report `
  * [x] Report Players and Users
  * [x] Report vulnerabilities/bugs
- [x] Ticketing system
  1. Simple command or button to create ticket
  1. ticket categories 
- [ ] Mod application system
  * Question 'modules'
    - multiple choice
    - yes/no
    - free answer
  * Configurable per guild
  * Different position applications (guild configurable)
- [ ] Reaction Roles
- [ ] User Levelling system
  * [ ] Points system based on messages sent in qualifying channels
  * [ ] Levels system based on points
  * [ ] `/level`: check own level and points
  

### Other Features
#### Bot Management
- [x] Cogs
  - [x] Load Cogs
  - [x] Unload Cogs
  - [x] Reload Cogs
- [x] Shutdown bot correctly (instead of just an exit)
- [ ] Check `config/config.yml` against `config/exampleconfig.yml` and add missing options to `config.yml`


#### Messages & Variables
- [x] Load most reused messages from yaml
- [x] Get bot token from yaml
- [x] Get role and guild IDs from db
- [x] Guild-specific settings system via db
