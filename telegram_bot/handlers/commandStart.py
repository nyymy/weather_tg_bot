from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from .questions_for_new_user import handle_location
from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove
from telegram_bot.keyboard.start_for_registered_user_kb import start_for_reg_user_kb
from telegram_bot.keyboard.start_kb import start_kb
from telegram_bot.Utils.database import Database
import os

router = Router()


@router.message(F.text.casefold() == "HI")
@router.message(CommandStart())
async def cmd_start(message: Message):
    db = Database(os.getenv("DATABASE_NAME"))
    users = db.select_user_id(message.from_user.id)
    if (users):
        await message.answer(f"Hello {users[1]}!\nChoose command to continue 🔽", reply_markup=start_for_reg_user_kb())
    else:
        await message.answer("Hello! Tap /location to continue", reply_markup=start_kb())
