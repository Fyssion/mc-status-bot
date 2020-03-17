import discord
from discord.ext import commands

class HelpCommand(commands.MinimalHelpCommand):
    def get_command_signature(self, command):
        return '`{0.clean_prefix}{1.qualified_name} {1.signature}`'.format(self, command)

class Meta(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self._default_help_command = bot.help_command
        bot.help_command = HelpCommand()
        bot.help_command.cog = self

    def cog_unload(self):
        self.bot.help_command = self._default_help_command


def setup(bot):
    bot.add_cog(Meta(bot))