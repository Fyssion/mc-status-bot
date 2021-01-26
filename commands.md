---
layout: default
nav_order: 3
---

# Commands

This list assumes your bot's prefix is `;`.<br>

Make sure to remove `<>` and `[]` when using a command.
{: .note }

- `;help` - View all commands.
  * `;help <command>` - Get help on a specific command or category.
- `;server` - View stats and info about the current Minecraft server.
  * `;server set <ip>` - Set the current Minecraft server.
    This will edit the config file for you.

    Example: `;server set mc.hypixel.net`
- `;players` - Get a list of all players on the Minecraft server.
  At the moment, this only works with Java servers.
- `;logout` - Logout and shutdown the bot.

  If the `;players` command isn't working,
  make sure to enable `enable-query` in your Minecraft server's `server.properties`.
  {: .note }

## Status Key

When the bot is...<br>
**Online** - Minecraft server is online and joinable.<br>
**Idle** - Minecraft server is online, but full.<br>
**DND** - Minecraft server is offline or closed.

The activity shows the current player count. Ex: `77/100 online`
