import discord
from discord.ext import commands


class Admin(commands.Cog):
    """Bot admin commands.

    Only the owner of the bot can use these commands.
    """

    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return await commands.is_owner().predicate(ctx)

    @commands.command(name="logout", aliases=["shutdown"])
    async def logout(self, ctx):
        """Logout and shutdown the bot.
        You must be the owner of the bot to use this command.
        """
        await ctx.send("Logging out...")
        await self.bot.close()


def setup(bot):
    bot.add_cog(Admin(bot))
