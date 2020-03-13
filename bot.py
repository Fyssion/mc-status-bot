import discord
from discord.ext import commands, tasks

import yaml
import logging


def get_prefix(client, message):
    prefixes = [";"]
    return commands.when_mentioned_or(*prefixes)(client, message)


class ServerStatus(commands.Bot):

    def __init__(self):
        super().__init__(
            command_prefix=get_prefix,
            description="Fetches and displays the status of a Minecraft server",
            case_insensitive=True,
            help_command = None,
        )

        logging.basicConfig(level=logging.INFO)

        self.config = self.load_config("config.yml")

        self.load_extension("cogs.status")
        self.load_extension("cogs.updates")
        try:
            self.load_extension("jishaku")
        except Exception as e:
            pass

    def load_config(self, filename):
        with open(filename, "r") as config:
            try:
                return yaml.safe_load(config)
            except yaml.YAMLError as exc:
                logging.critical("Could not load config.yml")
                print(exc)
                import sys
                sys.exit()

    async def on_ready(self):
        logging.info(f"Logged in as {self.user.name} - {self.user.id}")

    def run(self):
        super().run(self.config["bot-token"])


bot = ServerStatus()
bot.run()
