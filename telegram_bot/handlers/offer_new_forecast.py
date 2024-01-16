import os
from aiogram import Router, F
from aiogram.types import Message
from Utils.database import Database
from Utils.Message_builder import MessageBuilder
from keyboard.offer_new_forecast_kb import offer_new_forecast_kb


router = Router()


@router.message(F.text.contains("days forecast"))
async def offer_new_forecast(message: Message):
    db = Database(os.getenv("DATABASE_NAME"))
    lat = db.select_user_lat(message.from_user.id)[0]
    lon = db.select_user_lon(message.from_user.id)[0]
    days = int(message.text.split(' ')[0])
    message_builder = MessageBuilder(lat=lat, lon=lon, days=days)
    text_message = message_builder.create_message_text()
    image = message_builder.image_creator()
    await message.answer(f"{text_message}", reply_markup=offer_new_forecast_kb(days))
    await message.answer_photo(photo=image)

@router.message(F.text.startswith("Current"))
async def give_todays_weather(message: Message):
    db = Database(os.getenv("DATABASE_NAME"))
    lat = db.select_user_lat(message.from_user.id)[0]
    lon = db.select_user_lon(message.from_user.id)[0]
    days = 1
    message_builder = MessageBuilder(lat=lat, lon=lon, days=days)
    text_message = message_builder.create_message_text()
    await message.answer(f"{text_message}", reply_markup=offer_new_forecast_kb(days))
