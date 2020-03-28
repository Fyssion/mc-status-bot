import discord
from discord.ext import commands

from datetime import datetime as d
import logging
import json


class StatusEmbed:

    color = discord.Color.green()
    status = "Online"

    def __init__(self, channel: discord.TextChannel, status_message="No message provided."):
        self.channel = channel
        self.status_message = status_message

    def create_embed(self, message):
        em = discord.Embed(title=f"Server Status - {self.status}",
                           description=message, color=self.color)
        em.set_footer(text="This status message is managed by the server operator.")
        return em

    async def send(self):
        embed = self.create_embed(self.status_message)
        await self.channel.send(embed=embed)


class OnlineEmbed(StatusEmbed):

    def __init__(self, channel: discord.TextChannel, status_message="All is well!"):
        super().__init__(channel, status_message)


class MaintenenceEmbed(StatusEmbed):

    color = discord.Color.red()
    status = "Under Maintenence"

    def __init__(self, channel: discord.TextChannel,
                 status_message="Currently under maintenence. Server may or may not be online."):
        super().__init__(channel, status_message)


class ClosedEmbed(StatusEmbed):

    color = discord.Color.red()
    status = "Closed"

    def __init__(self, channel: discord.TextChannel,
                 status_message="Server is closed."):
        super().__init__(channel, status_message)



class DifficultiesEmbed(StatusEmbed):

    color = discord.Color.gold()
    status = "Experiencing Difficulties"

    def __init__(self, channel: discord.TextChannel, status_message="Currently experiencing difficulties."):
        super().__init__(channel, status_message)


class ServerOwners(commands.Cog, name="Server Owners"):
    """This module is for server owners who would like to update the status of their server manually."""

    def __init__(self, bot):
        self.bot = bot

        if "updates-channel" in bot.config.keys():
            channel = bot.config["updates-channel"]
            if channel:
                self.channel = self.bot.get_channel(int(channel))
        else:
            bot.config["updates-channel"] = None
            with open("config.json", "w") as config:
                json.dump(bot.config, config, indent=4, sort_keys=True)

    @commands.group(invoke_without_command=True, aliases=["update"])
    async def updates(self, ctx):
        if not self.channel:
            return await ctx.send("Updates are not enabled.")
        await ctx.send(f"Current updates channnel: {self.channel}")

    @updates.command(description="Enable server updates")
    @commands.has_permissions(manage_guild=True)
    async def enable(self, ctx, channel: discord.TextChannel = None):
        def check(ms):
            return ms.author.id == ctx.guild.me.id
        if not channel:
            await ctx.send("Auto setup isn't developed yet. Please specify a channel.")
        permissions = channel.permissions_for(ctx.guild.me)
        if not permissions.embed_links or not permissions.send_messages:
            return await ctx.send("Bot must have send messages and embed links in the updates channel.")
        self.channel = channel
        self.bot.config["updates-channel"] = channel.id
        with open("config.json", "w") as config:
                json.dump(self.bot.config, config, indent=4, sort_keys=True)
        await self.channel.purge(check=check)
        status_embed = OnlineEmbed(self.channel)
        await status_embed.send()

    @updates.command(description="Disable updates")
    @commands.has_permissions(manage_guild=True)
    async def disable(self, ctx):
        if not self.channel:
            return await ctx.send("Updates are already disabled.")
        self.channel = None
        del self.bot.config["updates-channel"]
        with open("config.json", "w") as config:
                json.dump(self.bot.config, config, indent=4, sort_keys=True)
        await ctx.send("Disabled updates")

    @updates.command(name="set", description="Set the current status")
    @commands.has_permissions(manage_guild=True)
    async def _set(self, ctx, status, *, message=None):
        def check(ms):
            return ms.author.id == ctx.guild.me.id
        if not self.channel:
            return await ctx.send("You must enable the updates first.")
        permissions = self.channel.permissions_for(ctx.guild.me)
        if not permissions.embed_links or not permissions.send_messages:
            return await ctx.send("Bot must have send messages and embed links in the updates channel.")
        if status.lower() == "online":
            if message:
                status_embed = OnlineEmbed(self.channel, message)
            else:
                status_embed = OnlineEmbed(self.channel)

        elif status.lower() in ["offline", "maintenence"]:
            if message:
                status_embed = MaintenenceEmbed(self.channel, message)
            else:
                status_embed = MaintenenceEmbed(self.channel)

        elif status.lower() in ["buggy", "difficulties"]:
            if message:
                status_embed = DifficultiesEmbed(self.channel, message)
            else:
                status_embed = DifficultiesEmbed(self.channel)

        elif status.lower() == "closed":
            if message:
                status_embed = ClosedEmbed(self.channel, message)
            else:
                status_embed = ClosedEmbed(self.channel)

        else:
            return await ctx.send("That is an invalid status.")

        await self.channel.purge(check=check)
        await status_embed.send()

        await ctx.send("Updated status!")


def setup(bot):
    bot.add_cog(ServerOwners(bot))