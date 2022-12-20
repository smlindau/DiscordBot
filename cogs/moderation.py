"""
Modified from https://github.com/kkrypt0nn (https://krypton.ninja)
"""
import discord
from discord import app_commands, HTTPException
from discord.ext import commands
from discord.ext.commands import Context

from helpers import checks, db_manager
from bot import config


class Moderation(commands.Cog, name="moderation"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="nick",
        description="Change the nickname of a user on a server.",
    )
    @app_commands.guilds(config["guild_id"])
    @commands.has_permissions(manage_nicknames=True)
    @commands.bot_has_permissions(manage_nicknames=True)
    @checks.not_blacklisted()
    @app_commands.describe(
        user="The user that should have a new nickname.",
        nickname="The new nickname that should be set.",
    )
    async def nick(
        self, context: Context, user: discord.User, *, nickname: str = None
    ) -> None:
        """
        Change the nickname of a user on a server.

        Parameters
        ----------
        context : Context
            The hybrid command context.
        user : discord.User
            The user that should have its nickname changed.
        nickname : str, optional
            The new nickname of the user. Default is None, which will reset the
            nickname.

        Returns
        -------
        None
        """
        member = context.guild.get_member(user.id) or await context.guild.fetch_member(
            user.id
        )
        try:
            await member.edit(nick=nickname)
            embed = discord.Embed(
                title="Changed Nickname!",
                description=f"**{member}'s** new nickname is **{nickname}**!",
                color=0x9C84EF,
            )
            await context.send(embed=embed)
        except HTTPException:
            embed = discord.Embed(
                title="Error!",
                description="An error occurred while trying to change the nickname of "
                "the user. Make sure my role is above the role of the user you want to "
                "change the nickname.",
                color=0xE02B2B,
            )
            await context.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Moderation(bot))
