from aiogram.fsm.state import State, StatesGroup
from py_dto import DTO
import os
import requests


class Userdata(DTO):
    lat: float
    lon: float
    days: int


class Form(StatesGroup):
    location = State()
    days = State()


class OpenWeatherApi:

    # three_day_api = f""
    # ten_day_api = f"daily?lat={self.lat}&lon={self.lon}&cnt={self.days}&appid={self.key}"
    def __init__(self, userdata: Userdata):
        self.key = os.getenv("Open_weather_key")
        self.lat = round(userdata.lat, 2)
        self.lon = round(userdata.lon, 2)
        self.days = userdata.days
        self.three_day_api = f"hourly?lat={self.lat}&lon={self.lon}&appid={self.key}"
        self.url = "https://api.openweathermap.org/data/2.5/forecast/"

    def get_data(self):
        print(f"{self.url}{self.three_day_api}")
        response = requests.get(url=self.url + self.three_day_api)
        print(response.text)
        print(response)
        return response.text
