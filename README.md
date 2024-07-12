<div align="center"><a href="https://github.com/TulipSMP/Tiramisu"><img src='src/tiramisu.png' alt='Tiramisu, an italian cake with coffee, chocolate, and creamy white icing. Drawn in a simplistic square ' width=200></a>
<h1> Tiramisu </h1>
<a href="https://github.com/TulipSMP/Tiramisu/actions/workflows/pylint.yml"><img src="https://github.com/TulipSMP/Tiramisu/actions/workflows/pylint.yml/badge.svg?branch=main&event=push" alt="Lint"></a>
</div>


An open source discord bot for all audiences, developed by the folks at Tulip SMP.

### ⚠️ Not Ready for Production
This bot is not finished, and is far from useable. In the meantime, feel free to open a pull request to help us out.

### URI Change

Make sure to update your local clone of the repo, with the following command:
```
git remote set-url origin https://github.com/TulipSMP/Tiramisu.git
```

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
- [x] Logging of the following actions:
  * [x] Message Deletion
  * [x] Message Edit
  * [x] VC Join/Leave
  * [x] VC Start/Stop streaming/camera
- [x] Ticketing system
  * Simple command to create ticket
  * Button to create ticket
- [x] Mod application system
  * Configurable per guild questions
  * Simple command to apply
  * Button to apply
- [x] User Levelling system
  * [x] Points system based on messages sent in qualifying channels
  * [x] Levels system based on points
  * [x] `/level`: check own level and points


### Other Features
#### Bot Management
- [x] Cogs
  - [x] Load Cogs
  - [x] Unload Cogs
  - [x] Reload Cogs
- [x] Shutdown bot correctly (instead of just an exit)
- [x] Check `config/config.yml` against `config/exampleconfig.yml` and add missing options to `config.yml`

#### Platform Links *Planned For Future Release*
- [ ] Two-way websocket-based chat bridge (between Tiramisu and third-party client) to other platforms (i.e. Minecraft)

#### Messages & Variables
- [x] Load most reused messages from yaml
- [x] Get bot token from yaml
- [x] Get role and guild IDs from db
- [x] Guild-specific settings system via db

## License

All source code is provided under the terms of the BSD-3-clause license.

Assets provided in the `src/` directory are provided under the terms of Creative Commons CC0 1.0 Universal.
