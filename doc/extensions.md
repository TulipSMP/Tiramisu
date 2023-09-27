# Extensions

Tiramisu has an extensions system which allows users and developers to add functionality to the bot without interfering with its other functions.

## Creating extensions

Extensions are Nextcord cogs with a few added options to integrate into Tiramisu. Here are the additional things that you must define in your file:

- `settings`: a list of strings, which contain the names of settings you want to have added to the database.
- `settings_hidden`: a list of strings as above, but that the user cannot see in the `/setting` commands, but can be used internally. 


#### Example

```python
# Example Extension
from logging42 import logger

import nextcord
from nextcord.ext import commands

import yaml

from libs.database import Database

class Extension(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        logger.info('Loaded Example extension!')

    # Commands
    @nextcord.slash_command(description="This is an Extension!")
    async def extension(self, interaction: nextcord.Interaction):
        db = Database(interaction.guild, reason="Extension")
        text = db.fetch('extension_text')
        
        try:
            uses = str(int(db.fetch('extension_uses_int')) + 1)
        except ValueError:
            uses = 1

        if text.strip() == 'none':
            text = "This command was from an extension!"
        text += f'\n*This command has been used {uses} times.*'
        await interaction.response.send_message(text)

# Extension Stuff

# Nextcord Cog Setup
def setup(bot):
    bot.add_cog(Extension(bot))

# Tiramisu Settings
settings = [
    'extension_text',
]
settings_hidden = [
    'extension_uses_int',
]
```