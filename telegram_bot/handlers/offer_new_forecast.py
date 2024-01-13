import os
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from telegram_bot.Utils.database import Database
from telegram_bot.Utils.Weather_data import WeatherData
from telegram_bot.Utils.Message_creater import MessageCreator
from telegram_bot.keyboard.offer_new_forecast_kb import offer_new_forecast_kb
from telegram_bot.Utils.Form import Form
router = Router()


@router.message(F.text.contains("days forecast"))
async def offer_new_forecast(message: Message):
    db = Database(os.getenv("DATABASE_NAME"))
    lat = db.select_user_lat(message.from_user.id)[0]
    lon = db.select_user_lon(message.from_user.id)[0]
    days = int(message.text.split(' ')[0])
    weather_data = WeatherData(lat=lat, lon=lon, days=days)
    dataframe_rounded = weather_data.get_forecast()
    forecast = MessageCreator(dataframe_rounded, lat=lat, lon=lon, days=days)
    await message.answer(f"{forecast.create_message()}", reply_markup=offer_new_forecast_kb(days))


@router.message(F.text.startswith("Current"))
async def give_todays_weather(message: Message):
    db = Database(os.getenv("DATABASE_NAME"))
    lat = db.select_user_lat(message.from_user.id)[0]
    lon = db.select_user_lon(message.from_user.id)[0]
    days = 1
    weather_data = WeatherData(lat=lat, lon=lon, days=days)
    dataframe_rounded = weather_data.get_forecast()
    forecast = MessageCreator(dataframe_rounded, lat=lat, lon=lon, days=days)
    await message.answer(f"{forecast.create_message()}", reply_markup=offer_new_forecast_kb(days))
