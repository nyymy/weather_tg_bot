from aiogram.utils.keyboard import ReplyKeyboardBuilder


def start_kb():
    kb = ReplyKeyboardBuilder()
    kb.button(text="/location")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True, one_time_keyboard=True,
                        input_field_placeholder="Choose command to continue 🔽")
