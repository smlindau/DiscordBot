"""
Modified from https://github.com/kkrypt0nn (https://krypton.ninja)
"""
import json
from typing import Callable, TypeVar

from discord.ext import commands

from exceptions import UserNotOwner, UserBlacklisted
from helpers import db_manager

T = TypeVar("T")


def is_owner() -> Callable[[T], T]:
    """
    This function executes a custom check to see if the user executing the command is
    an owner of the bot.

    Returns
    -------
    Callable bool
        True if user is an owner of the bot.

    Raises
    ------
    UserNotOwner
        Raised if the user is not an owner of the bot
    """

    async def predicate(context: commands.Context) -> bool:
        with open("config.json") as file:
            data = json.load(file)
        if context.author.id not in data["owners"]:
            raise UserNotOwner
        return True

    return commands.check(predicate)


def not_blacklisted() -> Callable[[T], T]:
    """
    This function executes a custom check to see if the user executing the command is
    not blacklisted.

    Returns
    -------
    Callable bool
        True if the user is not blacklisted.

    Raises
    ------
    UserBlacklisted
        Raised if the user is blacklisted.
    """

    async def predicate(context: commands.Context) -> bool:
        if await db_manager.is_blacklisted(context.author.id):
            raise UserBlacklisted
        return True

    return commands.check(predicate)
