from aiogram import Router, F
from aiogram.types import Message
from telegram_bot.Utils.Weather_data import WeatherData
from telegram_bot.Utils.Message_creater import MessageCreator
from aiogram.filters.command import Command
from telegram_bot.keyboard.offer_new_forecast_kb import offer_new_forecast_kb
from telegram_bot.keyboard.location_kb import share_location_kb
from telegram_bot.keyboard.day_count_kb import number_of_days_kb
from telegram_bot.Utils.Form import Form, Userdata
from aiogram.utils.markdown import hbold
from aiogram.fsm.context import FSMContext
import os
from telegram_bot.Utils.database import Database
router = Router()


# api_call = f"api.openweathermap.org/data/2.5/forecast/daily?lat={Form.lat}&lon={Form.lon}&cnt={Form.days}&appid={API_key}"


@router.message(Command("location"))
async def cmd_locate_me(message: Message, state: FSMContext):
    await state.set_state(Form.location)
    reply = "Click  on the the button below to share your location"
    await message.answer(reply, reply_markup=share_location_kb())


@router.message(F.location, Form.location)
async def handle_location(message: Message, state: FSMContext):
    user = message.from_user
    location = (message.location.latitude, message.location.longitude)
    await state.update_data(location=location)
    await state.set_state(Form.days)
    print(f"{Form.location}")
    reply = f'Thank you, {hbold(user.first_name)}! Choose for how many days forecast do u need? Click the button'
    await message.reply(reply, reply_markup=number_of_days_kb())


@router.message(Form.days, F.text.casefold() == "10")
@router.message(Form.days, F.text.casefold() == "3")
async def three_days_forecast(message: Message, state: FSMContext):
    await state.update_data(days=message.text)
    data = await state.get_data()
    await state.clear()

    userdata = Userdata({
        "lat": data.get("location")[0],
        "lon": data.get("location")[1],
        "days": int(data.get("days")),
    })
    db = Database(os.getenv('DATABASE_NAME'))
    users = db.select_user_id(message.from_user.id)
    if not users:
        db.add_user(message.from_user.first_name, userdata.lat, userdata.lon, message.from_user.id)
    weather_data = WeatherData(lat=userdata.lat, lon=userdata.lon, days=userdata.days)
    dataframe_rounded = weather_data.get_forecast()
    forecast = MessageCreator(dataframe_rounded, lat=userdata.lat, lon=userdata.lon, days=userdata.days)
    await message.answer(f"{forecast.create_message()}", reply_markup=offer_new_forecast_kb(userdata.days))


@router.message(Form.days)
async def ten_days_forecast(message: Message, state: FSMContext):
    await message.answer("Choose between 3 or 10")
