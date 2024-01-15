import os
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from Utils.database import Database
from Utils.Weather_data import WeatherData
from Utils.Message_creater import MessageCreator
from keyboard.offer_new_forecast_kb import offer_new_forecast_kb
from Utils.Form import Form
from aiogram.types import FSInputFile

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
    forecast.create_graphic()
    image = FSInputFile(f"Utils/graph{days}.png")
    await message.answer(f"{forecast.create_message()}", reply_markup=offer_new_forecast_kb(days))
    await message.answer_photo(photo=image)

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
