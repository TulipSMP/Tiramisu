# Getting Started

First, clone this repository. To do so, run the following command:

```sh
git clone https://github.com/RoseSMP/Tiramisu.git
```
If you want to also clone our custom cogs specific to RoseSMP, run the following command instead:
```sh
git clone --recurse-submodules https://github.com/RoseSMP/Tiramisu.git
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


## Running

Running the bot is as simple as running one command:
```sh
python3 bot.py
```
