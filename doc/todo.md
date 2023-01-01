# Feature Parity (and Roadmap) Between various bot solutions
* Proprietary: Fizz wasted money on this one imo, but it gets the job done. current rosebot and fizzv2 bots
* Rosebotv2: Fizz made this one. Good job!
* Tiramisu: Krafter and fizzdev are working on this one, not near complete (or even 50%)
* Red: cool, foss, GPLv3, modular & python (we could even make our own cogs for this one)

# Comparison

| Bot:      | **Proprietary** | **rosebotv2** | **Tiramisu** | **Red** |
| --------- | --------------- | ------------- | ------------ | ------- |
| License   | Proprietary     | MPL 2.0       | MIT          | GPLv3   |
| Language  | Urmom           | Python        | Python       | Python  |
| Library   | Deez nutz       | Nextcord      | Nextcord  | Discord.py |
| Host      | Self            | Self          | Self         | Self    |
| **Feature Set** |           |               |              |         |
| New Discord API | Yes       | Yes           | Yes          | No      |
| Reaction Roles | Yes        | Yes (iirc)    | Todo         | Yes     |
| Tickets   | Yes             | No            | Todo         | ?       |
| Warns     | Yes             | Yes (no DM)   | Todo         | ?       |
| Applications[¹](#1)| Yes    | No            | Todo         | ?       |
| Polls     | No              | No            | Todo         | ?       |
| Announce[²](#2)| Yes        | Yes           | Todo         | ?       |
| Giveaway  | Yes             | No            | Todo         | ?       |


<!--
TODO.md todo:
 - add links to red docs & cogs
 - check for red's feature set
-->

----------

#### Footnotes
##### 1 
Like tickets, but ask questions to fill out a form. Could also be used to collect statistics, or run quizzes for giveaways
##### 2
Send a message in a predefined channel via command, useful for mods and admins sending announcements or changelogs