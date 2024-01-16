import os
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hbold
from keyboard.offer_new_forecast_kb import offer_new_forecast_kb
from keyboard.location_kb import share_location_kb
from keyboard.day_count_kb import number_of_days_kb
from Utils.database import Database
from Utils.Message_builder import MessageBuilder
from Utils.Form import Form, Userdata

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
    message_builder = MessageBuilder(lat=userdata.lat, lon=userdata.lon, days=userdata.days)
    text_message = message_builder.message_text
    image = message_builder.image
    await message.answer(f"{text_message}", reply_markup=offer_new_forecast_kb(userdata.days))
    await message.answer_photo(photo=image)


@router.message(Form.days)
async def ten_days_forecast(message: Message, state: FSMContext):
    await message.answer("Choose between 3 or 10")
