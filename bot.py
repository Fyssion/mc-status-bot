import discord
from discord.ext import commands, tasks

import json
import logging


def get_prefix(client, message):
    with open("config.json", "r") as f:
        config = json.load(f)
    prefixes = [config["prefix"]]
    return commands.when_mentioned_or(*prefixes)(client, message)


class ServerStatus(commands.Bot):

    def __init__(self):
        super().__init__(
            command_prefix=get_prefix,
            description="Fetches and displays the status of a Minecraft server",
            case_insensitive=True,
        )

        logging.basicConfig(level=logging.INFO)

        self.config = self.load_config("config.json")

        self.load_extension("cogs.meta")
        self.load_extension("cogs.status")
        self.load_extension("cogs.server_owners")
        try:
            self.load_extension("jishaku")
        except Exception as e:
            pass

    def load_config(self, filename):
        with open(filename, "r") as config:
            return json.load(config)

    async def on_ready(self):
        logging.info(f"Logged in as {self.user.name} - {self.user.id}")

    def run(self):
        super().run(self.config["bot-token"])


bot = ServerStatus()
bot.run()
