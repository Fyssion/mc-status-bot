---
layout: default
nav_order: 1
---

# Installation

The following page guides you through the installation process.

**If you have any issues during installation, join the [support server](https://www.discord.gg/eHxvStNJb7) on Discord.**
[![Discord server invite](https://discord.com/api/guilds/682053500775170120/embed.png)](https://discord.gg/eHxvStNJb7)

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
        - If you're unsure on how to create a bot application, [read this tutorial](https://discordpy.readthedocs.io/en/latest/discord.html).
      - Check [configuration]({{ site.url }}/configuration) for more info on the rest of the options.

4. Run the bot
   - On Windows, run `run.bat` and on Mac/Linux run `run.sh`
     - Note that you need to keep the bot running in order for it to keep displaying the status.<br>
       If you can't host the bot on your machine, I recommend renting a cheap VPS to run the bot on.
