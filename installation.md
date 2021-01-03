---
layout: default
nav_order: 1
---

# Installation

The following page guides you through the installation process.

**If you have any issues during installation, join the [support server]({{ site.discord_server }}) on Discord.**
[![Discord server invite](https://discord.com/api/guilds/682053500775170120/embed.png)](https://discord.gg/eHxvStNJb7)

If you don't download the bot as a Git repository (using the steps below),
you will get an error when running the bot.
{: .warn }

1. Clone the repository (as a Git repository).
    - You must have Git installed to install and run the bot.
        * [Download Git here.](https://git-scm.com/downloads)
    - Once you have Git installed, download the bot with a command (in CMD or a terminal):<br>
      `git clone https://github.com/Fyssion/mc-status-bot.git`

2. Install dependencies and setup the bot.
    - Python 3.6+ is required to run the bot. Python 3.7+ is recommended. [Download Python here.](https://www.python.org/downloads/)
    - Once you have python installed, run `updater.bat` on Windows or `updater.sh` on Mac/Linux.
        * The updater will download all the dependencies for the bot and update you to the latest version.<br>
          Run the updater whenever you need to update the bot or need help changing config options.
    - When the updater is done updating the bot, it will initiate the setup.
        * The `token` is the how the bot logs into Discord, which you get from a bot application.
            - If you're unsure on how to create a bot application, [read this tutorial.](https://discordpy.readthedocs.io/en/latest/discord.html).
        * Check [configuration]({{ "/configuration" | relative_url  }}) for more info on the rest of the options.

4. Run the bot
      - On Windows, run `run.bat` and on Mac/Linux run `run.sh`.


You need to keep the bot running in order for it to keep displaying the status.<br>
If you can't host the bot on your machine, I recommend renting a cheap VPS to run the bot on.
{: .note }


## What's next?

If you want to configure the bot further, checkout [configuration]({{ "/configuration" | relative_url  }}).
Otherwise, if you want to view the bot's commands, head to [commands]({{ "/commands" | relative_url  }}).
