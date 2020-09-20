import discord
from discord.ext import commands

import yaml
import logging

formatter = logging.Formatter("[%(levelname)s] %(name)s: %(message)s")
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
        super().__init__(
            command_prefix=get_prefix,
            description=description,
            case_insensitive=True,
            activity=discord.Game("Starting up..."),
            help_command=commands.MinimalHelpCommand(),
        )

        self.log = log

        log.info("Starting bot...")

        log.info("Reading config file...")
        self.config = self.load_config("config.yml")

        log.info("Loading extensions...")
        for extension in initial_extensions:
            self.load_extension(extension)

        try:
            self.load_extension("jishaku")

        except Exception:
            log.info("jishaku is not installed, continuing...")

    def load_config(self, filename):
        with open(filename, "r") as f:
            return yaml.safe_load(f)

    async def on_ready(self):
        log.info(f"Logged in as {self.user.name} - {self.user.id}")

    def run(self):
        super().run(self.config["bot-token"])


if __name__ == "__main__":
    bot = ServerStatus()
    bot.run()
