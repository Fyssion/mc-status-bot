# Minecraft Server Status Bot

![Online Status Example for mc.hypixel.net](images/online.png)
![Full Status Example](images/full.png)
![Offline Status Example](images/offline.png)

A simple Discord bot that displays the status of a Minecraft server in the sidebar.

**If you have any issues, join the [support server](https://www.discord.gg/wfCGTrp) on Discord.**
[![Discord server invite](https://discord.com/api/guilds/682053500775170120/embed.png)](https://discord.gg/wfCGTrp)

## Features

- "At a glance" status display; no need to boot up Minecraft to see who's online!
- Real-time Minecraft server status
- Customizable prefix
- Easy-to-follow setup instructions
- Custom maintenance mode detection
- A support server to help with setup or issues

## Commands

Make sure to remove <> and [] when using a command.

- `;help` - View all commands
  - `;help <command>` - Get help on a specific command or category
- `;server` - View info about the current Minecraft server
  - `;server set <ip>` - Set the current Minecraft server
- `;players` - Get a list of all players on the Minecraft server

## Status Key

**Online** - Minecraft server is online and joinable<br>
**Idle** - Minecraft server is online, but full<br>
**DND** - Minecraft server is offline or closed

The activity shows the current player count. Ex: 77/100 online

## Installation

**If you have any issues during installation, join the [support server](https://www.discord.gg/wfCGTrp) on Discord.**
[![Discord server invite](https://discord.com/api/guilds/682053500775170120/embed.png)](https://discord.gg/wfCGTrp)

1. Clone the repository (as a Git repo)
   - You must have Git installed to install and run the bot
     - [Download Git here](https://git-scm.com/downloads)
   - Once you have Git installed, download the bot with a command (in CMD or a terminal):
     - `git clone https://github.com/Fyssion/mc-status-bot.git`
   - *If you don't download the bot as a Git repo (using the steps above), you will not be able to run the bot*
2. Install dependencies and setup the bot
   - Python 3.6+ is required to run the bot. Python 3.7+ is recommended. [Download Python here](https://www.python.org/downloads/)
   - Once you have python installed, run `updater.bat` on Windows or `updater.sh` on Mac/Linux.
     - The updater will download all the dependencies for the bot and update you to the latest version.<br>
       Run the updater whenever you need to update the bot or need help changing config options.
    - When the updater is done updating the bot, it will initiate the setup.
      - The `token` is the how the bot logs into Discord, which you get from a bot application.
        - If you're unsure on how to create a bot application, [visit this website](https://discordpy.readthedocs.io/en/latest/discord.html).
      - Check the [table below](#setup-details) for more info on the rest of the options.
4. Run the bot
   - On Windows, run `run.bat` and on Mac/Linux run `run.sh`
     - Note that you need to keep the bot running in order for it to keep displaying the status.<br>
       If you can't host the bot on your machine, I recommend renting a cheap VPS to run the bot on.

### Setup details

The table below describes each option in the setup config.
If you are confused, please ask in the [support server](https://www.discord.gg/wfCGTrp).

| Option                       | Description                                                                                                                                                                                                                                                                                   | Default               |
|------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------|
| `bot-token`                  | This is the how the bot logs into Discord, which you get from a bot application. If you're unsure on how to create a bot application, [visit this website](https://discordpy.readthedocs.io/en/latest/discord.html).                                                                          | No Default (required) |
| `prefix`                     | The prefix for the bot. This is used at the beginning of each command.                                                                                                                                                                                                                        | ;                     |
| `server-ip`                  | The Minecraft server IP to display the status for.                                                                                                                                                                                                                                            | No Default (required) |
| `refresh-rate`               | The time in seconds in between status refreshes. Cannot be less than 30.                                                                                                                                                                                                                      | 60                    |
| `maintenance-mode-detection` | Whether or not to run maintenance mode detection. This essentially looks for the specified word in the server's MOTD, and if it is found it sets the status to maintenance mode (DND). Example: setting the value to `maintenance` will look for the word "maintenance" in the server's MOTD. | Disabled              |

## Requirements

- discord.py>=1.4.1
- mcstatus
- pyyaml
- OPTIONAL: jishaku

## Attributes

- [Just-Some-Bots/MusicBot](https://github.com/Just-Some-Bots/MusicBot) for run and updater scripts. Copyright (c) Just-Some-Bots
