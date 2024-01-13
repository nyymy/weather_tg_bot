from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def number_of_days_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="3")
    kb.button(text="10")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True, one_time_keyboard=True, input_field_placeholder="Choose 3 or 10 below")

