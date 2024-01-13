import openmeteo_requests
import requests_cache
from .WindDirectoinReform import degrees_to_compass
from .cloud_percentage_to_emoji import cloud_percentage_to_emoji
from .swap_digits_with_emojis import swap_digits_with_emojis
from Utils.get_local_time import get_local_time


class MessageCreator:
    def __init__(self, dataframe_rounded, lat, lon, days):
        self.__lat = lat
        self.__lon = lon
        self.__days = days
        self.__dataframe_rounded = dataframe_rounded

    def create_message(self):
        if self.__days == 3:
            message = self.__create_message_for_three_days()
        elif self.__days == 10:
            message = self.__create_message_for_ten_days()
        elif self.__days == 1:
            message = self.__create_message_for_current()
        return message

    def __create_message_for_current(self):
        temp = self.__dataframe_rounded["cur_temperature"]
        cloud_cover = cloud_percentage_to_emoji(self.__dataframe_rounded["cur_cloud_cover"])
        wind_speed = self.__dataframe_rounded["cur_wind_speed"]
        wind_direction = degrees_to_compass(self.__dataframe_rounded["cur_wind_direction"])

        message = f"Current weather:\n🌡️{temp}°C, 💨{wind_direction} {wind_speed}km/h, {cloud_cover}"
        return message

    def __create_message_for_three_days(self):

        hourly_data_formatted = []
        current_day = None

        for index, row in self.__dataframe_rounded.iterrows():
            # print(row)
            date = row['date']
            formatted_date = date.strftime('%d %A')
            time = date.strftime('%H:%M')
            temperature = row['temperature_2m']
            precipitation_probability = row['precipitation_probability']
            cloud_cover = cloud_percentage_to_emoji(row['cloud_cover'])
            wind_speed_10m = row['wind_speed_10m']
            wind_direction_10m = degrees_to_compass(row['wind_direction_10m'])

            message = (f"    {time} 🌡️{temperature}°C, ~{precipitation_probability}%💧, {cloud_cover}, "
                       f"💨{wind_direction_10m} {wind_speed_10m}km/h")

            # Check if the day has changed
            if formatted_date != current_day:
                current_day = formatted_date
                formatted_data = (
                    f"{swap_digits_with_emojis(formatted_date)}:\n{message}")
            else:
                formatted_data = message
            hourly_data_formatted.append(formatted_data)
            formatted_output = '\n'.join(hourly_data_formatted)

        return formatted_output

    def __create_message_for_ten_days(self):
        daily_data_formatted = []
        for index, row in self.__dataframe_rounded.iterrows():
            # print(row)
            date = row['date']
            time = swap_digits_with_emojis(date.strftime('%d '))
            day_of_the_week = date.strftime('%A')
            temperature_max = row['temperature_2m_max']
            temperature_min = row['temperature_2m_min']
            precipitation_probability = row['precipitation_probability_max']
            wind_speed_10m = row['wind_speed_10m_max']
            wind_direction_10m = degrees_to_compass(row['wind_direction_10m_dominant'])

            message = (f"{time} {day_of_the_week}🌡️{temperature_min}°C min - 🌡️{temperature_max}°C max, "
                       f" ~{precipitation_probability}%💧, 💨{wind_direction_10m} {wind_speed_10m}km/h")

            # Check if the day has changed
            formatted_data = message
            daily_data_formatted.append(formatted_data)
            formatted_output = '\n'.join(daily_data_formatted)

        return formatted_output
