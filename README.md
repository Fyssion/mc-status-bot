# Minecraft Server Status Bot

Discord Bot that checks status for a specified server and displays it in the Discord sidebar.

## Installation

1. Clone the repository
   - Press the green `Clone or download` button, and click on Download ZIP
   - Extract the ZIP file
2. Install requirements (listed in the Requirements section)
   - Python is required to run the bot. [Download Python here](https://www.python.org/downloads/)
   - Once you have python installed, you can use `py -m pip install -U REQUIREMENT_HERE` (replace `py` with `python` on Linux and Mac)
   - Use the command above in cmd (or terminal on Linux and Mac).
      You can add all the requirements to the end of the command, seperated by spaces.
   - You could also use the command separately for each requirement
3. Create a config.yml file (with notepad or your prefered text editor), and paste this in (make sure to fill in the values):
   ```yml
   bot-token: BOT-TOKEN-HERE
   server-url: SERVER-URL-HERE
   ```
   - If you're unsure on how to create a bot application, [visit this website](https://discordpy.readthedocs.io/en/latest/discord.html).
4. Run bot.py
   - It's recommended you run bot.py in cmd.
   - On Windows, you navigate to the folder where you have the bot, open CMD (shift right click, click `Open Powershell window here`)
   - Type `py bot.py` to start the bot.
   
## Commands

- `;set` - Set the server to get status from
- `;ip` - View the IP of the current server
- `;players` - Get a list of the players on the server (APPEARS TO BE BROKEN)
- `;enable` - Enable updates (see Setup Updates section below)
- `;update` - Update the updates message with a new one (see Setup Updates section below)

## Setup Updates (after installation)

Make sure you have installed the bot correctly and are running `bot.py`.
The bot should appear online and should be showing the server's status.

After you have confirmed the bot is installed correctly, follow these steps to set up updates:

1. Create a channel. Call it whatever you like.
2. Set the channel permissions so the status bot has send messages and embed links.
3. Use the `;enable CHANNEL_HERE` command, replacing `CHANNEL_HERE` with the channel you just created.
4. You can use the updates feature with the `;update STATUS_HERE MESSAGE_HERE` command.
   - `STATUS_HERE` can be online, offline, maintenance, buggy, or difficulties.
   - `MESSAGE_HERE` can be left blank. This will set the message to the default.

## Requirements

- discord.py==1.3.2
- mcstatus
- pyyaml
- OPTIONAL: jishaku
