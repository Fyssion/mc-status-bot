import discord
from discord.ext import commands, tasks

from mcstatus import MinecraftServer
from datetime import datetime as d
import logging
import yaml


class Status(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.server = MinecraftServer.lookup(self.bot.config["server-url"])
        if not self.server:
            logging.critical("Could not find server.")
            import sys
            sys.exit()
        self.current_status = [None, None]
        self.update_status.start()

    def cog_unload(self):
        self.update_status.cancel()

    @commands.command(description="Get player list for the current server",
                      aliases=["list", "who", "online"])
    async def players(self, ctx):
        return await ctx.send("That command is still in development.")
        try:
            status = self.server.status()
        except:
            return await ctx.send("Server is offline.")
        players = "\n".join(status.players.names)
        em = discord.Embed(title=f"Current Players Online:", description=players,
                           color=discord.Color.green(), timestamp=d.utcnow())
        port = self.server.port if self.server.port != 25565 else ""
        em.set_footer(text=f"Server IP: {self.server.host}:{port}")

    @commands.command(name="set", hidden=True)
    @commands.is_owner()
    async def _set(self, ctx, domain):
        server = MinecraftServer.lookup(domain)
        if not server:
            return await ctx.send("Could not find that server")
        self.server = server
        self.bot.config["server-url"] = domain
        with open("config.yml", "w") as config:
            yaml.dump(self.bot.config, config)

    @tasks.loop(seconds=15)
    async def update_status(self):
        try:
            status = self.server.status()

        except:
            game = discord.Game("Server is Offline")
            if self.current_status == [discord.Status.dnd, game]:
                return
            await self.bot.change_presence(status=discord.Status.dnd, acivity=game)
            self.current_status = [discord.Status.dnd, game]
            return

        if status.players.online == status.players.max:
            bot_status = discord.Status.idle
        else:
            bot_status = discord.Status.online
        game = discord.Game(f"{status.players.online}/{status.players.max} players online")
        if self.current_status == [bot_status, game]:
            return
        await self.bot.change_presence(status=bot_status, activity=game)
        self.current_status = [bot_status, game]

    @update_status.before_loop
    async def before_printer(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(Status(bot))
