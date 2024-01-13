import asyncio
import logging
import sys
import os

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from handlers.questions_for_new_user import router as questions_router
from handlers.offer_new_forecast import router as offer_router
from handlers.commandStart import router as start_router
from handlers.forecast_for_registered_user import router as registered_user_router
from Utils.commands import set_commands


load_dotenv()

token = os.getenv("TELEGRAM_TOKEN_POPLAVSKIY")
bot = Bot(token=token, parse_mode=ParseMode.HTML)
dp = Dispatcher()
list_of_routers = [start_router, questions_router, offer_router, registered_user_router]
dp.include_routers(*list_of_routers)


async def start() -> None:
    await set_commands(bot)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(start())
