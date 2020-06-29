import discord
from discord.ext import commands, tasks

from mcstatus import MinecraftServer
from datetime import datetime as d
import functools
import logging
import json



class Status(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        if "server-url" in self.bot.config.keys():
            self.bot.config["server-ip"] = self.bot.config["server-url"]
            del self.bot.config["server-url"]
            with open("config.json", "w") as config:
                json.dump(self.bot.config, config, indent=4, sort_keys=True)

        self.server = MinecraftServer.lookup(self.bot.config["server-ip"])
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
        query_server = MinecraftServer(self.server.host, 25565)
        partial = functools.partial(query_server.query)
        try:
            query = await self.bot.loop.run_in_executor(None, partial)
        except Exception as e:
            return await ctx.send("Server is offline or does not have query set up.\n"
                                  "Activate query with `enable-query` in server.properties.\n"
                                  f"```py\n{e}\n```")
        players = "\n".join(query.players.names)
        em = discord.Embed(title=f"Current Players Online:", description=players,
                           color=discord.Color.green(), timestamp=d.utcnow())
        port = self.server.port if self.server.port != 25565 else ""
        em.set_footer(text=f"Server IP: {self.server.host}:{port}")
        await ctx.send(embed=em)

    @commands.group(description="Get the ip of the current server",
                    invoke_without_command=True, aliases=["ip"])
    async def server(self, ctx):
        await ctx.send(f"IP: **`{self.bot.config['server-ip']}`**")

    @server.command(name="set")
    @commands.is_owner()
    async def _set(self, ctx, domain):
        server = MinecraftServer.lookup(domain)
        if not server:
            return await ctx.send("Could not find that server")
        self.server = server
        self.bot.config["server-ip"] = domain
        with open("config.json", "w") as config:
            json.dump(self.bot.config, config, indent=4, sort_keys=True)
        await ctx.send(f"Set status to {domain}")

    @commands.Cog.listener("on_connect")
    async def reload_status(self):
        if not self.bot.is_ready():
            return
        partial = functools.partial(self.server.status)
        try:
            status = await self.bot.loop.run_in_executor(None, partial)

        except:
            game = discord.Game("Server is offline")
            await self.bot.change_presence(status=discord.Status.dnd, activity=game)
            self.current_status = [discord.Status.dnd, game]
            return

        if status.players.online == status.players.max:
            bot_status = discord.Status.idle
        else:
            bot_status = discord.Status.online
        game = discord.Game(f"{status.players.online}/{status.players.max} online")
        await self.bot.change_presence(status=bot_status, activity=game)
        self.current_status = [bot_status, game]

    def get_game(self, game):
        if not game:
            return None
        return game.name

    @tasks.loop(seconds=15)
    async def update_status(self):
        partial = functools.partial(self.server.status)
        try:
            status = await self.bot.loop.run_in_executor(None, partial)
        except:
            game = discord.Game("Server is offline")
            if self.current_status == [discord.Status.dnd, game] and self.bot_member.activity:
                return
            await self.bot.change_presence(status=discord.Status.dnd, activity=game)
            self.current_status = [discord.Status.dnd, game]
            return

        if status.players.online == status.players.max:
            bot_status = discord.Status.idle
        else:
            bot_status = discord.Status.online
        game = discord.Game(f"{status.players.online}/{status.players.max} online")
        if self.current_status == [bot_status, game] and self.bot_member.activity:
            return
        await self.bot.change_presence(status=bot_status, activity=game)
        self.current_status = [bot_status, game]

    async def get_bot_member(self):
        if not self.bot.guilds:
            return None
        return self.bot.guilds[0].get_member(self.bot.user.id)

    @update_status.before_loop
    async def before_printer(self):
        await self.bot.wait_until_ready()
        self.bot_member = await self.get_bot_member()


def setup(bot):
    bot.add_cog(Status(bot))
