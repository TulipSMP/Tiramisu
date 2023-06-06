# help.py
A help menu for Tiramisu, accessible in discord

### `config/help.yml`

Contains the information for the help screen. It contains the various topics and their contents, to be sent to the user when they use the `/help` slash command in discord. 

#### Layout
Each help topic has a `name` field, the pretty name of that topic displayed to the user, and a `contents` field, the actual message to send to the user.

The only required help topic is `main`, which is used if no help topic is specified.

Example `config/help.yml`:
```yml
main:
  name: Main
  contents: |
    # Help
    Here's some help...

more-help:
  name: Get More Help
  contents: |
    # More Help
    More help information...
```

Additionally, before sending the message, `[[BOT]]` is replaced with the bot's username whenever it occurs in `contents`.

#### Guidelines
Help topics should be short and to-the-point, giving users the information they need quickly and effectively. Discord's (limited) markdown should be used to highlight titles and other sections so that users can quickly find the information they need.


### Slash Command
```
/help topic:[topic]
```
The `topic` options are generated when the cog is loaded, based on `config/help.yml`. `main` is used if `topic:` is not specified.