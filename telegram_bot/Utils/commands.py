from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description="Get Forecast"
        ),
        BotCommand(
            command="location",
            description="Share your location"
        )
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())
