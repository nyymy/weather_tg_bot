import os

from aiogram import Router, F
from aiogram.types import Message

from telegram_bot.Utils.database import Database
from telegram_bot.Utils.Weather_data import WeatherData
from telegram_bot.Utils.Message_creater import MessageCreator
from telegram_bot.keyboard.day_count_kb import number_of_days_kb
from telegram_bot.keyboard.offer_new_forecast_kb import offer_new_forecast_kb
from telegram_bot.keyboard.location_kb import share_location_kb

router = Router()


@router.message(F.location)
async def choose_day(message: Message):
    user = message.from_user
    new_lat = message.location.latitude
    new_lon = message.location.longitude
    db = Database(os.getenv("DATABASE_NAME"))
    db.update_user_location(user.id, new_lat, new_lon)
    await message.answer("⭐OK! Choose for how many days forecast do u need? Click the button",
                         reply_markup=number_of_days_kb())


@router.message(F.text.startswith("Use previous location"))
async def choose_day(message: Message):
    await message.answer("⭐OK! Choose for how many days forecast do u need? Click the button",
                         reply_markup=number_of_days_kb())


@router.message(F.text.startswith("Use new location"))
async def choose_location(message: Message):
    reply = "Click  on the the button below to share your location"
    await message.answer(reply, reply_markup=share_location_kb())


@router.message(F.text.casefold() == "10")
@router.message(F.text.casefold() == "3")
async def give_forecast(message: Message):
    db = Database(os.getenv("DATABASE_NAME"))
    lat = db.select_user_lat(message.from_user.id)[0]
    lon = db.select_user_lon(message.from_user.id)[0]
    days = int(message.text)
    weather_data = WeatherData(lat=lat, lon=lon, days=days)
    dataframe_rounded = weather_data.get_forecast()
    forecast = MessageCreator(dataframe_rounded, lat=lat, lon=lon, days=days)
    await message.answer(f" here is\n{forecast.create_message()}", reply_markup=offer_new_forecast_kb(days))
