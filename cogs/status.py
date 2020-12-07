import discord
from discord.ext import commands, tasks

from mcstatus import MinecraftServer
import asyncio
import functools
import logging
import yaml
import traceback
import datetime
import io
import re
import base64


log = logging.getLogger("bot")


class ServerNotFound(commands.CommandError):
    def __init__(self, ip):
        self.ip = ip

        super().__init__(f"Could not find server with an IP of {ip}.")


class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.activity = None
        self.status = None

        self.last_set = None

        self.ip = ip = self.bot.config["server-ip"]
        log.info(f"Looking up Minecraft server IP: {ip}")
        self.server = MinecraftServer.lookup(ip)

        if not self.server:
            log.critical(f"Could not find server with an IP of {ip}.")
            raise ServerNotFound(ip)

        log.info(f"Found server with an IP of {ip}")

        self.status_updater_task.change_interval(seconds=bot.config["refresh-rate"])
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
            async with ctx.typing():
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
            title="Current Players Online:",
            description=players,
            color=discord.Color.green(),
        )

        em.set_footer(text=f"Server IP: `{self.ip}`")
        await ctx.send(embed=em)

    def resolve_favicon(self, status):
        if status.favicon:
            string = ",".join(status.favicon.split(",")[1:])
            bytes = io.BytesIO(base64.b64decode(string))
            bytes.seek(0)

            return discord.File(bytes, "favicon.png")

        return None

    @commands.group(
        invoke_without_command=True,
        aliases=["ip"],
    )
    async def server(self, ctx):
        """Get info about the current server"""
        partial = functools.partial(self.server.status)
        try:
            async with ctx.typing():
                status = await self.bot.loop.run_in_executor(None, partial)

        except Exception:
            status = None
            color = discord.Color.red()
            status_text = "Offline"

        else:

            players = f"{status.players.online}/{status.players.max}"

            if status.players.online == status.players.max:
                color = discord.Color.orange()
                status_text = f"Full - {players}"
            else:
                color = discord.Color.green()
                status_text = f"Online - {players}"

        if status:
            motd = self._parse_motd(status)
            if len(motd) > 1024:
                motd = motd[:1024] + "..."

        else:
            motd = ""

        em = discord.Embed(title="Minecraft Server Info", description=motd, color=color)
        em.add_field(name="IP", value=f"`{self.ip}`")
        em.add_field(name="Status", value=status_text)

        file = None

        if status:
            em.add_field(name="Version", value=status.version.name)
            em.add_field(name="Latency", value=status.latency)

            favicon = self.resolve_favicon(status)
            if favicon:
                em.set_thumbnail(url="attachment://favicon.png")
                file = favicon

        await ctx.send(embed=em, file=file)

    @server.command(name="set")
    @commands.is_owner()
    async def server_set(self, ctx, ip):
        """Set the IP for the server via command.

        This will automatically update the config file.
        """
        partial = functools.partial(MinecraftServer.lookup, ip)

        async with ctx.typing():
            server = await self.bot.loop.run_in_executor(None, partial)

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
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def update(self, ctx):
        """Manually update the status if it broke"""
        await self.update_status(force=True)
        await ctx.send("Updated status")

    async def set_status(self, status, text, *, force=False):
        game = discord.Game(text)

        # We only want to send a request if the status is different
        # or if the status is not set.
        # The below returns if either of those requirements are not met.
        now = datetime.datetime.utcnow()
        if (
            not force
            and self.last_set
            and self.last_set + datetime.timedelta(minutes=30) < now
            and self.activity == game
            and self.status == status
        ):
            return

        await self.bot.change_presence(status=status, activity=game)
        self.status = status
        self.activity = game

        log.info(f"Set status to {status}: {text}")

    def _parse_motd(self, server):
        if isinstance(server.description, dict):
            description = server.description.get("text", "")
            extras = server.description.get("extra")
            if extras:
                for extra in extras:
                    description += extra.get("text", "")

        else:
            description = str(server.description)

        description = re.sub(r"§.", "", description)

        return description

    async def get_status(self):
        partial = functools.partial(self.server.status)
        try:
            server = await self.bot.loop.run_in_executor(None, partial)

        except Exception:
            return discord.Status.dnd, "Server is offline"

        if server.players.online == server.players.max:
            status = discord.Status.idle
        else:
            status = discord.Status.online

        maintenance_text = self.bot.config["maintenance-mode-detection"]
        if maintenance_text:
            # somehow some people have this not as a string
            if not isinstance(maintenance_text, str):
                logging.warning(
                    "maintenance-mode-detection has been set, but is not a vaild type. "
                    f"It must be a string, but is a {type(maintenance_text)} instead."
                )
                return None

            # I guess the status can be a dict?
            description = self._parse_motd(server)

            if maintenance_text.lower() in description.lower():
                return discord.Status.dnd, "Server is in maintenence mode"

        return status, f"{server.players.online}/{server.players.max} online"

    async def update_status(self, *, force=False):
        status, text = await self.get_status()

        await self.set_status(status, text, force=force)

    @tasks.loop(seconds=60)
    async def status_updater_task(self):
        await self.update_status()

    @status_updater_task.before_loop
    async def before_printer(self):
        await self.bot.wait_until_ready()
        log.info("Waiting 10 seconds before next status set")
        await asyncio.sleep(10)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        if len(self.guilds) == 1:
            log.info("Joined first guild, setting status")
            await self.update_status()


def setup(bot):
    bot.add_cog(Status(bot))
