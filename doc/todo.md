# Feature Parity (and Tiramisu Roadmap) Between various bot solutions
* Proprietary [CoreBot](https://corebot.dev/): Fizz wasted money on this one imo, but it gets the job done. current rosebot and fizzv2 bots
* [Rosebotv2](https://github.com/fizzrepo/rosebot): Fizz made this one. Good job!
* [Tiramisu](https://github.com/RoseSMP/Tiramisu): Krafter and fizzdev are working on this one, not near complete (or even 50%)
* [Red](https://github.com/Cog-Creators/Red-DiscordBot): cool, anime, foss, GPLv3, modular & python (we could even make our own cogs for this one)

## Bot Comparison

| Bot:      | **CoreBot**     | **rosebotv2** | **Tiramisu** | **Red** |
| --------- | --------------- | ------------- | ------------ | ------- |
| License   | Proprietary     | MPL 2.0       | MIT          | GPLv3   |
| Language  | Urmom           | Python        | Python       | Python  |
| Library   | Deez nutz       | Nextcord      | Nextcord  | Discord.py |
| Host      | Self            | Self          | Self         | Self    |
| **Feature Set** |           |               |              |         |
| New Discord API | Yes       | Yes           | Yes          | No      |
| Reaction Roles | Yes        | Yes           | Todo         | ?       |
| Tickets   | Yes             | No            | Todo         | [Yes](https://github.com/NeuroAssassin/Toxic-Cogs/tree/master/reacticket) |
| Applications[¹](#1)| Yes    | No            | Todo         | No      |
| Polls     | No              | No            | Todo         | [Yes](https://github.com/flapjax/FlapJack-Cogs/tree/red-v3-rewrites/msgvote) |
| Announce[²](#2)| Yes        | Yes           | Todo         | [Yes](https://github.com/Obi-Wan3/OB13-Cogs/tree/main/announcements) |
| Giveaway  | Yes             | No            | Todo         | [Yes](https://github.com/flaree/flare-cogs/tree/master/giveaways) / [Yes](https://github.com/Redjumpman/Jumper-Plugins/tree/V3/raffle) |
| Suggestions/Bug Reports | Yes | No          | Todo         | [Yes](https://github.com/flapjax/FlapJack-Cogs/tree/red-v3-rewrites/msgvote) |
| **Moderation** |            |               |              |         |
| Rules Reference[³](#3) | No | No            | Todo         | Yes     |
| Warns     | Yes             | Yes (no DM)   | Todo         | Yes     |
| Bans      | Yes             | Yes           | Todo         | Yes     |

<!--
TODO.md todo:
 - add links to red docs & cogs
 - check for red's feature set
-->

----------

#### Footnotes
##### 1 
Like tickets, but ask questions to fill out a form. Could also be used to collect statistics, or run quizzes for giveaways. Has the following input methods:
 - Text (reply with message)
 - Multiple Choice
 - Boolean
##### 2
Send a message in a predefined channel via command, useful for mods and admins sending announcements or changelogs.
##### 3
Set a #rules channel, set your rules (the bot will post them there). You can edit them later, and use them for ban or warn reasons.