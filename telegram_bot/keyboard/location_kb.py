from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def share_location_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="📍 share location", request_location=True)
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True, one_time_keyboard=True, input_field_placeholder="Press the button ⬇️")
