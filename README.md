# Minecraft Server Status Bot

![Online Status Example for mc.hypixel.net](images/online.png)
![Full Status Example](images/full.png)
![Offline Status Example](images/offline.png)

A Discord bot that displays the status of a Minecraft server in the sidebar.

**If you have any issues, join the [support server](https://www.discord.gg/wfCGTrp) on Discord.** 

## Features

- "At a glance" status display; no need to boot up Minecraft to see who's online!
- Real-time Minecraft server status
- Customizable prefix
- Easy-to-follow setup instructions
- A support server to help with setup or issues

## Commands

- `;help` - View all commands
  - `;help <command>` - Get help on a specific command
- `;server` - View current server's IP
  - `;server set <ip>` - Set the server to get status from
- `;players` - Get a list of the players on the server (APPEARS TO BE BROKEN)

## Status Key

**Online** - Minecraft server is online and joinable

**Idle** - Minecraft server is online, but full

**DND** - Minecraft server is offline or closed

The activity shows the current player count. Ex: 77/100 online

## Installation

1. Clone the repository
   - Press the green `Clone or download` button, and click on Download ZIP
   - Extract the ZIP file
2. Install requirements (listed in the Requirements section)
   - Python is required to run the bot. [Download Python here](https://www.python.org/downloads/)
   - Once you have python installed, you can use `py -m pip install -U -r requirements.txt` (replace `py` with `python3` on Linux and Mac)
     - You must be in the bot's directory for this to work. Use `cd DIRECTORY_HERE` with the bot's directory. 
   - Use the command above in cmd (or terminal on Linux and Mac).
3. Create a config.json file in the bot's directory (with notepad or your preferred text editor), and paste this in (make sure to fill in the values):

   ```yml
   bot-token: BOT_TOKEN_HERE
   prefix: PREFIX_HERE
   server-ip: SERVER_IP_HERE
   ```

   - BOT_TOKEN_HERE is the bot's token, which you get from a bot application.
     - If you're unsure on how to create a bot application, [visit this website](https://discordpy.readthedocs.io/en/latest/discord.html).
   - PREFIX_HERE is the bot's prefix (e.g. ! or ?)
   - SERVER_IP_HERE is the IP of the server you want to display (e.g. mc.hypixel.net)
4. Run bot.py
   - It's recommended you run bot.py in a terminal (e.g. cmd).
   - On Windows, you navigate to the folder where you have the bot, open CMD (shift right click, click `Open Powershell window here`)
   - Type `py bot.py` to start the bot.

## Requirements

- discord.py>=1.4.1
- mcstatus
- pyyaml
- OPTIONAL: jishaku
