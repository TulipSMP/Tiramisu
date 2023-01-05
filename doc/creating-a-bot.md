# Creating a Discord Bot

This guide shows how to create a discord bot user for tiramisu to use on your server.


## 1. Enter the Portal

Go to [discord.com/developers](https://discord.com/developers/) and log in to your discord account.


## 2. Create an 'Application'

In the top righthand side of the page, click the big button that says "New Application". Then, enter a name for your bot and check the checkbox to agree to discord's [Developer Terms of Service](https://discord.com/developers/docs/policies-and-agreements/terms-of-service) and [Developer Policy](https://discord.com/developers/docs/policies-and-agreements/developer-policy).

Now, click "Create"!

You can enter a description and upload a profile pic if you want, or continue (you can always come back to this bit later).


## 3. Make it a Bot!

On the left pane, click "Bot" and then click the big "Add Bot" button under "Build-A-Bot".

Under 'Authorization Flow' make sure 'Requires OAUTH2 Code Grant' is turned off, and turn on all the switches under 'Priveleged Gateway Intents'.


## 4. Get the Token

On the Bot page, click 'Reset Token' under 'Token' (near the top). Confirm by clicking 'Yes, do it!'. You may have to enter your password or a 2FA code. Now, click 'Copy' and paste that value into your bot's [`config/config.yml`](../config/config.yml).