"""
Modified from https://github.com/kkrypt0nn (https://krypton.ninja)
"""
import discord
from discord import app_commands, HTTPException
from discord.ext import commands
from discord.ext.commands import Context

from helpers import checks, db_manager
from bot import config


class Owner(commands.Cog, name="owner"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="sync",
        description="Synchronizes the slash commands.",
    )
    @app_commands.describe(scope="The scope of the sync. Can be `global` or `guild`")
    @checks.is_owner()
    async def sync(self, context: Context) -> None:
        """
        Synchronizes the slash commands.

        Parameters
        ----------
        context : Context
            The hybrid command context.

        Returns
        -------
        None
        """
        await context.bot.tree.sync()
        embed = discord.Embed(
            title="Slash Commands Sync",
            description="Slash commands have been globally synchronized.",
            color=0x9C84EF,
        )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="load",
        description="Load a cog",
    )
    @app_commands.guilds(config["guild_id"])
    @app_commands.describe(cog="The name of the cog to load")
    @checks.is_owner()
    async def load(self, context: Context, cog: str) -> None:
        """
        The boat will load the given cog.

        Parameters
        ----------
        context : Context
            The hybrid command context.
        cog : str
            The name of the cog to load.

        Returns
        -------
        None
        """
        try:
            await self.bot.load_extension(f"cogs.{cog}")
        except HTTPException:
            embed = discord.Embed(
                title="Error!",
                description=f"Could not load the `{cog}` cog.",
                color=0xE02B2B,
            )
            await context.send(embed=embed)
            return
        embed = discord.Embed(
            title="Load",
            description=f"Successfully loaded the `{cog}` cog.",
            color=0x9C84EF,
        )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="unload",
        description="Unloads a cog.",
    )
    @app_commands.guilds(config["guild_id"])
    @app_commands.describe(cog="The name of the cog to unload")
    @checks.is_owner()
    async def unload(self, context: Context, cog: str) -> None:
        """
        The bot will unload the given cog.

        Parameters
        ----------
        context : Context
            The hybrid command context.
        cog : str
            The name of the cog to unload.

        Returns
        -------
        None
        """
        try:
            await self.bot.unload_extension(f"cogs.{cog}")
        except HTTPException:
            embed = discord.Embed(
                title="Error!",
                description=f"Could not unload the `{cog}` cog.",
                color=0xE02B2B,
            )
            await context.send(embed=embed)
            return
        embed = discord.Embed(
            title="Unload",
            description=f"Successfully unloaded the `{cog}` cog.",
            color=0x9C84EF,
        )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="reload",
        description="Reloads a cog.",
    )
    @app_commands.guilds(config["guild_id"])
    @app_commands.describe(cog="The name of the cog to reload")
    @checks.is_owner()
    async def reload(self, context: Context, cog: str) -> None:
        """
        The bot will reload the given cog.

        Parameters
        ----------
        context : Context
            The hybrid command context.
        cog : str
            The name of the cog to reload.

        Returns
        -------
        None
        """
        try:
            await self.bot.reload_extension(f"cogs.{cog}")
        except HTTPException:
            embed = discord.Embed(
                title="Error!",
                description=f"Could not reload the `{cog}` cog.",
                color=0xE02B2B,
            )
            await context.send(embed=embed)
            return
        embed = discord.Embed(
            title="Reload",
            description=f"Successfully reloaded the `{cog}` cog.",
            color=0x9C84EF,
        )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="shutdown",
        description="Make the bot shutdown.",
    )
    @app_commands.guilds(config["guild_id"])
    @checks.is_owner()
    async def shutdown(self, context: Context) -> None:
        """
        Shuts down the bot.

        Parameters
        ----------
        context : Context
            The hybrid command context.

        Returns
        -------
        None
        """
        embed = discord.Embed(description="Shutting down. Bye! :wave:", color=0x9C84EF)
        await context.send(embed=embed)
        await self.bot.close()

    @commands.hybrid_group(
        name="blacklist",
        description="Get the list of all blacklisted users.",
    )
    @app_commands.guilds(config["guild_id"])
    @checks.is_owner()
    async def blacklist(self, context: Context) -> None:
        """
        Lets you add or remove a user from not being able to use the bot.

        Parameters
        ----------
        context : Context
            The hybrid command context.

        Returns
        -------
        None
        """
        if context.invoked_subcommand is None:
            embed = discord.Embed(
                title="Blacklist",
                description="You need to specify a subcommand.\n\n**Subcommands:**\n"
                "`add` - Add a user to the blacklist.\n"
                "`remove` - Remove a user from the blacklist.",
                color=0xE02B2B,
            )
            await context.send(embed=embed)

    @blacklist.command(
        base="blacklist",
        name="add",
        description="Lets you add a user to a blacklist, blocking their access to the "
        "bot",
    )
    @app_commands.guilds(config["guild_id"])
    @app_commands.describe(user="The user that should be added to the blacklist")
    @checks.is_owner()
    async def blacklist_add(self, context: Context, user: discord.User) -> None:
        """
        Lets you add a user to a blacklist, blocking their access to the bot.

        Parameters
        ----------
        context : Context
            The hybrid command context.
        user : discord.User
            The user that should be added to the blacklist.

        Returns
        -------
        None
        """
        user_id = user.id
        if await db_manager.is_blacklisted(user_id):
            embed = discord.Embed(
                title="Error!",
                description=f"**{user.name}** is not in the blacklist.",
                color=0xE02B2B,
            )
            await context.send(embed=embed)
            return
        total = await db_manager.add_user_to_blacklist(user_id)
        embed = discord.Embed(
            title="User Blacklisted",
            description=f"**{user.name}** has been successfully added to the blacklist",
            color=0x9C84EF,
        )
        embed.set_footer(
            text=f"There are now {total} {'user' if total == 1 else 'users'} in the "
            f"blacklist "
        )
        await context.send(embed=embed)

    @blacklist.command(
        base="blacklist",
        name="remove",
        description="Lets you remove a user from not being able to use the bot.",
    )
    @app_commands.guilds(config["guild_id"])
    @app_commands.describe(user="The user that should be removed from the blacklist.")
    @checks.is_owner()
    async def blacklist_remove(self, context: Context, user: discord.User) -> None:
        """
        Lets you remove a user from not being able to use the bot.

        Parameters
        ----------
        context : Context
            The hybrid command context.
        user : discord.User
            The user that should be removed from the blacklist.

        Returns
        -------
        None
        """
        user_id = user.id
        if not await db_manager.is_blacklisted(user_id):
            embed = discord.Embed(
                title="Error!",
                description=f"**{user.name}** is already in the blacklist.",
                color=0xE02B2B,
            )
            await context.send(embed=embed)
            return
        total = await db_manager.remove_user_from_blacklist(user_id)
        embed = discord.Embed(
            title="User removed from blacklist",
            description=f"**{user.name}** has been successfully removed from the "
            f"blacklist",
            color=0x9C84EF,
        )
        embed.set_footer(
            text=f"There are now {total} {'user' if total == 1 else 'users'} in the "
            f"blacklist "
        )
        await context.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Owner(bot))
