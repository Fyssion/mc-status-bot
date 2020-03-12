import discord
from discord.ext import commands, tasks

from mcstatus import MinecraftServer
import yaml
import logging


class Status(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.server = MinecraftServer.lookup(self.bot.config["server-url"])
        if not self.server:
            logging.critical("Could not find server.")
            import sys
            sys.exit()
        self.update_status.start()

    def cog_unload(self):
        self.update_status.cancel()

    @tasks.loop(seconds=15)
    async def update_status(self):
        status = self.server.status()
        game = discord.Game(f"{status.players.online}/{status.players.max}")
        await self.bot.change_presence(activity=game)

    @update_status.before_loop
    async def before_printer(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(Status(bot))
