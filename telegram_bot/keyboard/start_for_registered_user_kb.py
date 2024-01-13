from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def start_for_reg_user_kb():
    kb = ReplyKeyboardBuilder()
    kb.button(text="Use previous location")
    kb.button(text="Use new location")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True, one_time_keyboard=True,
                        input_field_placeholder="Choose command to continue 🔽")
