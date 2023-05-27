# Running Automatically
How to have the bot autostart on systemd systems.

## 1. Make a bot user
The bot should not be run as root! This could potentially cause security risks. To create the user, run the following command:
```bash
sudo useradd -d /home/tiramisu -m -s /bin/bash -c "Tiramisu Discord Bot" tiramisu
```
Then, so services under this user autostart, run this command:
```bash
sudo loginctl enable-linger tiramisu
```

## 2. Install the bot
Login as the `tiramisu` user we created in the previous step, and set up the bot as per the instructions in the [Getting Started](getting-started.md) page.

This guide will assume you cloned the repo while in your home directory.

## 3. Create the systemd service
Create the directory to put the file in:
```bash
mkdir -p ~/.config/systemd/user/
```
Then, we'll make the file. Run this command:
```bash
nano ~/.config/systemd/user/tiramisu.service
```
In that file put the following:

```
[Unit]
Description=Tiramisu Discord Bot

[Service]
ExecStart=/usr/bin/python3 /home/tiramisu/Tiramisu/bot.py
WorkingDirectory=/home/tiramisu/Tiramisu

[Install]
WantedBy=default.target
```

You'll have to reload the systemd-daemon before systemd can see this file:
```bash
systemctl --user daemon-reload
```

Now, you can start and enable this service:
```bash
systemctl --user enable tiramisu.service
systemctl --user start tiramisu.service
```
To view tiramisu's logs:
```bash
journalctl --user -u tiramisu.service -b
```
Note: If the dates on the logs you see here look old, press `END` on your keyboard to go to the latest part of the log.
