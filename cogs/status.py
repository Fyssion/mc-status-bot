import discord
from discord.ext import commands, tasks

from mcstatus import MinecraftServer
import asyncio
import functools
import logging
import yaml
import traceback


log = logging.getLogger("bot")


class ServerNotFound(commands.CommandError):
    def __init__(self, ip):
        self.ip = ip
        super().__init__(f"Could not find server with an IP of {ip}.")


class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.ip = ip = self.bot.config["server-ip"]
        log.info(f"Looking up Minecraft server IP: {ip}")
        self.server = MinecraftServer.lookup(ip)

        if not self.server:
            log.critical(f"Could not find server with an IP of {ip}.")
            raise ServerNotFound(ip)

        log.info(f"Found server with an IP of {ip}")

        self.status_updater_task.start()

    def cog_unload(self):
        self.status_updater_task.cancel()

    @commands.command(
        aliases=["list", "who", "online"],
    )
    async def players(self, ctx):
        """Get player list for the current server"""
        partial = functools.partial(self.server.query)
        try:
            query = await self.bot.loop.run_in_executor(None, partial)

        except Exception as exc:
            traceback.print_exception(type(exc), exc, exc.__traceback__)
            return await ctx.send(
                "An error occured while attempting to query the server.\n"
                "Server may be offline or does not have query set up.\n"
                "Activate query with `enable-query` in `server.properties`.\n"
                f"Error: ```py\n{exc}\n```"
            )

        players = "\n".join(query.players.names)
        em = discord.Embed(
            title=f"Current Players Online:",
            description=players,
            color=discord.Color.green(),
        )

        em.set_footer(text=f"Server IP: `{self.ip}`")
        await ctx.send(embed=em)

    @commands.group(
        invoke_without_command=True,
        aliases=["ip"],
    )
    async def server(self, ctx):
        """Get the ip of the current server"""
        await ctx.send(f"IP: **`{self.ip}`**")

    @server.command(name="set")
    @commands.is_owner()
    async def _set(self, ctx, ip):
        """Set the IP for the server via command.

        This will automatically update the config file.
        """
        server = MinecraftServer.lookup(ip)
        if not server:
            return await ctx.send("Could not find that server")

        self.server = server
        self.ip = ip
        self.bot.config["server-ip"] = ip
        with open("config.yml", "w") as config:
            yaml.dump(self.bot.config, config, indent=4, sort_keys=True)

        await self.update_status()

        await ctx.send(f"Set server to `{ip}`.")

    @commands.command()
    async def update(self, ctx):
        """Manually update the status if it broke"""
        await self.update_status()
        await ctx.send("Updated status")

    def get_game(self, game):
        if not game:
            return None
        return game.name

    async def get_me(self):
        if not self.bot.guilds:
            return None

        return self.bot.guilds[0].me

    async def set_status(self, status, text):
        current_status = [status, text]

        me = await self.get_me()

        game = discord.Game(text)

        # We only want to send a request if the status is different
        # or if the status is not set.
        # The below returns if either of those requirements are not met.
        if me and me.activity == game and me.status == status:
            return

        await self.bot.change_presence(status=status, activity=game)
        self.current_status = current_status

        log.info(f"Set status to {status}: {text}")

    async def update_status(self):
        partial = functools.partial(self.server.status)
        try:
            server = await self.bot.loop.run_in_executor(None, partial)

        except Exception:
            await self.set_status(discord.Status.dnd, "Server is offline")
            return

        if server.players.online == server.players.max:
            status = discord.Status.idle
        else:
            status = discord.Status.online

        maintenance_text = self.bot.config["maintenance-mode-detection"]
        if maintenance_text:
            if maintenance_text.lower() in server.description.lower():
                await self.set_status(discord.Status.dnd, "Server is in maintenance mode")
                return

        await self.set_status(status, f"{server.players.online}/{server.players.max} online")

    @tasks.loop(seconds=60)
    async def status_updater_task(self):
        await self.update_status()

    @status_updater_task.before_loop
    async def before_printer(self):
        await self.bot.wait_until_ready()
        log.info("Waiting 10 seconds before initial status set")
        await asyncio.sleep(10)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        if len(self.guilds) == 1:
            log.info("Joined first guild, setting status")
            await self.update_status()


def setup(bot):
    bot.add_cog(Status(bot))
