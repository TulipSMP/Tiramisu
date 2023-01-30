# Getting Started

First, clone this repository. To do so, run the following command:

```sh
git clone -b prod https://github.com/RoseSMP/Tiramisu.git
```
(Omit the `-b prod` portion if you're doing development or testing changes)

Then, change into the directory:
```sh
cd Tiramisu/
```


## Installing

### Dependencies

For using this bot, you'll need to have `python` and `pip` installed. These packages are installed by default on most modern distributions. Then, you can install all dependencies with the following command (on most operating systems). 
```sh
pip install -r requirements.txt
```
if that doesn't work, make sure you have `pip` in your `$PATH`. Or, try this:
```sh
python3 -m pip install -r requirements.txt
```
If you're on ms windows, try this command:
```powershell
py -m pip install -r requirements.txt
```


### Database

You'll need a MySQL database running for this bot to store data in. If you don't know how to setup a MySQL database you can check [their documentation](https://dev.mysql.com/doc/mysql-getting-started/en/). 

After that's set up and running, edit the [config/config.yml](../config/config.yml) file (see [exampleconfig.yml](../config/exampleconfig.yml) for help) to apply to your instance.


## Configure

After MySQL is set up and running, you'll need to configure the bot. 

First, copy over the config file
```sh
cp config/exampleconfig.yml config/config.yml
```

#### MySQL
Open `config/config.yml` with an editor such as `nano` (like so: `nano config/config.yml`). Below is the first portion of the ymlfile:
```yml
mysql:
  host: 'localhost'
  port: '3306'
  user: 'tiramisu'
  pass: 'passwordSecure'
  db: 'tiramisu'
```
Make sure the `user` value is the user you want the bot to use to connect to your MySQL instance, and `pass` is the password it should use to connect. Set to `''` for a blank password. If your MySQL server is hosted on a seperate machine to that of the bot, you will want to change `host` to that of the machine running MySQL. `db` is the name of the database to connect to.


#### Bot Token

Here is the next part of `config.yml`:
```yml
discord:
  token: 'YourBotToken'
  owner: 00000000000000
  co_owners:
    - 00000000000000000000
    - 00000000000000000000
```
`token` is where you should put the token your bot uses to log in with. Replace `YourBotToken` with your bot's access token. If you don't know how to make a bot, read [this doc](creating-a-bot.md).

`owner` is the user ID of the person hosting this bot instance. They can add administrators and other things only the person hosting the bot should have permission to do.

`co_owners` are user IDs of other people you want to be able to load/unload cogs for your instance, and stop the bot. **Only put IDs here of people you trust, as they can ruin your bot via these commands**

After it's all configured, save and continue to the next step!
(If you're using `nano` type `Ctrl`+`o`,`Enter`, `Ctrl`+`x`, to save and quit.)

## Running

Running the bot is as simple as running one command:
```sh
python3 bot.py
```
See [Running Automatically](running-automatically.md) for how to autostart the bot on systemd systems.
