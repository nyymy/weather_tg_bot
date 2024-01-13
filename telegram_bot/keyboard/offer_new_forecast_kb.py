from aiogram.utils.keyboard import ReplyKeyboardBuilder


def offer_new_forecast_kb(days):
    kb = ReplyKeyboardBuilder()
    if days == 3:
        kb.button(text="10 days forecast")
    else:
        kb.button(text="3 days forecast")
    kb.button(text="Use new location")
    kb.button(text="Current weather")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True, one_time_keyboard=True)
