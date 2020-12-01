import discord
from discord.ext import commands

import yaml
import logging

discord.VoiceClient.warn_nacl = False  # don't need this warning

formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s", "%Y-%m-%d %H:%M:%S")
handler = logging.StreamHandler()
handler.setFormatter(formatter)

logger = logging.getLogger("discord")
logger.setLevel(logging.INFO)
logger.addHandler(handler)

log = logging.getLogger("bot")
log.setLevel(logging.INFO)
log.addHandler(handler)


initial_extensions = [
    "cogs.status",
]


def get_prefix(bot, message):
    prefixes = [bot.config["prefix"]]
    return commands.when_mentioned_or(*prefixes)(bot, message)


description = """
Discord Bot that checks status for a Minecraft server and displays it in the Discord sidebar
"""


class ServerStatus(commands.Bot):
    def __init__(self):
        intents = discord.Intents(messages=True, guilds=True, reactions=True)

        super().__init__(
            command_prefix=get_prefix,
            description=description,
            case_insensitive=True,
            activity=discord.Game("Starting up..."),
            help_command=commands.MinimalHelpCommand(),
            intents=intents,
        )

        self.log = log

        log.info("Starting bot...")

        log.info("Loading config file...")
        self.config = self.load_config("config.yml")

        log.info("Loading extensions...")
        for extension in initial_extensions:
            self.load_extension(extension)

        log.info("Setting initial status before logging in...")
        status_cog = self.get_cog("Status")
        status, text = self.loop.run_until_complete(status_cog.get_status())
        game = discord.Game(text)
        status_cog.activity = game

        self._connection._status = status
        self.activity = game

        self.init_ok = None
        self.restart_signal = None

        try:
            self.load_extension("jishaku")

        except Exception:
            log.info("jishaku is not installed, continuing...")

    def load_config(self, filename):
        with open(filename, "r") as f:
            return yaml.safe_load(f)

    async def on_command(self, ctx):
        destination = None

        if ctx.guild is None:
            destination = "Private Message"
        else:
            destination = f"#{ctx.channel} ({ctx.guild})"

        log.info(f"{ctx.author} in {destination}: {ctx.message.content}")

    async def on_ready(self):
        log.info(f"Logged in as {self.user.name} - {self.user.id}")
        self.init_ok = True

    def run(self):
        log.info("Logging into Discord...")
        super().run(self.config["bot-token"])


if __name__ == "__main__":
    bot = ServerStatus()
    bot.run()
