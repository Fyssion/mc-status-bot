---
layout: default
nav_order: 2
---

# Configuration

Configuring `mc-status-bot` is a breeze.

## Editing the config file

To edit the config file, simply run the updater. On Windows that's `updater.bat`, and on MacOS/Linux that's `updater.sh`.
Once the updater has finished updating the bot, it will ask you if you'd like to edit the config. Enter `y` and proceed.

Alternatively, you can edit the config file directly with a text editor.
The config file is `config.yml`, which is located in the bot's main directory.

If you do not see `config.yml`, make sure you
have run the updater. The updater will create and initialize the config file for you.<br>
Alternatively, you can create the `config.yml` file manually using the [example below.](#example-config)
{: .note }

Editing the config file directly may cause the bot to crash on startup. If this happens, don't panic!
There are restrictions on certain options. To see the restrictions, either see the [table below](#setup-details)
or use the config helper in the updater. 
{: .warn }

## Setup details

The table below describes each option in the setup config.

| Option                       | Description                                                                                                                                                                                                                                                                                   | Default               |
|------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------|
| `bot-token`                  | This is the how the bot logs into Discord, which you get from a bot application. If you're unsure on how to create a bot application, [visit this website](https://discordpy.readthedocs.io/en/latest/discord.html).                                                                          | No Default (required) |
| `prefix`                     | The prefix for the bot. This is used at the beginning of each command.                                                                                                                                                                                                                        | ;                     |
| `server-type`                | The type of Minecraft server. Can be either Java or Bedrock.                                                                                                                                                                                                                                  | Java                  |
| `server-ip`                  | The Minecraft server IP to display the status for.                                                                                                                                                                                                                                            | No Default (required) |
| `refresh-rate`               | The time in seconds in between status refreshes. Cannot be less than 30.                                                                                                                                                                                                                      | 60                    |
| `maintenance-mode-detection` | Whether or not to run maintenance mode detection. This essentially looks for the specified word in the server's MOTD, and if it is found it sets the status to maintenance mode (DND). Example: setting the value to `maintenance` will look for the word "maintenance" in the server's MOTD. | Disabled              |

## Example config

If you want to manually create the config file, here is what it should look like:

```yml
bot-token: BOT-TOKEN-HERE
maintenance-mode-detection: null
prefix: ;
refresh-rate: 60
server-ip: mc.hypixel.net
server-type: java
```
