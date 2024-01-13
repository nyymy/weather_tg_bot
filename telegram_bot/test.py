import openmeteo_requests
import requests_cache
import pandas as pd
from datetime import datetime
from retry_requests import retry
from tabulate import tabulate
from Utils.WindDirectoinReform import degrees_to_compass
from Utils.cloud_percentage_to_emoji import cloud_percentage_to_emoji
from Utils.swap_digits_with_emojis import swap_digits_with_emojis
from Utils.Weather_data import WeatherData
from Utils.Message_creater import MessageCreator
# Setup the Open-Meteo API client with cache and retry on error


# def give_table(lat, lon, days):
#     cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
#     retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
#     openmeteo = openmeteo_requests.Client(session=retry_session)
#     current_hour = datetime.now().hour
#
#     # Make sure all required weather variables are listed here
#     # The order of variables in hourly or daily is important to assign them correctly below
#     url = "https://api.open-meteo.com/v1/forecast"
#     params = {
#         "latitude": lat,
#         "longitude": lon,
#         "hourly": ["temperature_2m", "precipitation_probability", "cloud_cover", "wind_speed_10m",
#                    "wind_direction_10m"],
#         "daily": ["temperature_2m_max", "temperature_2m_min", "wind_speed_10m_max", "wind_direction_10m_dominant"],
#         "forecast_days": days,
#         "timezone": "auto"
#     }
#     responses = openmeteo.weather_api(url, params=params)
#
#     # Process first location. Add a for-loop for multiple locations or weather models
#     response = responses[0]
#     # print(f"Coordinates {response.Latitude()}°E {response.Longitude()}°N")
#     # print(f"Elevation {response.Elevation()} m asl")
#     # print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
#     # print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")
#
#     # Process hourly data. The order of variables needs to be the same as requested.
#     hourly = response.Hourly()
#     hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
#     hourly_precipitation_probability = hourly.Variables(1).ValuesAsNumpy()
#     hourly_cloud_cover = hourly.Variables(2).ValuesAsNumpy()
#     hourly_wind_speed_10m = hourly.Variables(3).ValuesAsNumpy()
#     hourly_wind_direction_10m = hourly.Variables(4).ValuesAsNumpy()
#
#     hourly_data = {"date": pd.date_range(
#         start=pd.to_datetime(hourly.Time(), unit="s"),
#         end=pd.to_datetime(hourly.TimeEnd(), unit="s"),
#         freq=pd.Timedelta(seconds=hourly.Interval()),
#         inclusive="left"
#     )}
#     hourly_data["temperature_2m"] = hourly_temperature_2m
#     hourly_data["precipitation_probability"] = hourly_precipitation_probability
#     hourly_data["cloud_cover"] = hourly_cloud_cover
#     hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
#     hourly_data["wind_direction_10m"] = hourly_wind_direction_10m
#
#     # print(hourly_dataframe)
#
#     # Process daily data. The order of variables needs to be the same as requested.
#     daily = response.Daily()
#     daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()
#     daily_temperature_2m_min = daily.Variables(1).ValuesAsNumpy()
#     daily_wind_speed_10m_max = daily.Variables(2).ValuesAsNumpy()
#     daily_wind_direction_10m_dominant = daily.Variables(3).ValuesAsNumpy()
#
#     daily_data = {"date": pd.date_range(
#         start=pd.to_datetime(daily.Time(), unit="s"),
#         end=pd.to_datetime(daily.TimeEnd(), unit="s"),
#         freq=pd.Timedelta(seconds=daily.Interval()),
#         inclusive="left"
#     )}
#     daily_data["temperature_2m_max"] = daily_temperature_2m_max
#     daily_data["temperature_2m_min"] = daily_temperature_2m_min
#     daily_data["wind_speed_10m_max"] = daily_wind_speed_10m_max
#     daily_data["wind_direction_10m_dominant"] = daily_wind_direction_10m_dominant
#     hourly_dataframe = pd.DataFrame(data=hourly_data)
#
#     hourly_dataframe_rounded = hourly_dataframe.map(lambda x: round(x, 1) if isinstance(x, (float, int)) else x)
#     hourly_data_formatted = []
#     current_day = None
#
#     for index, row in hourly_dataframe_rounded.iterrows():
#         date = row['date']
#         formatted_date = date.strftime('%d %A')
#         time = date.strftime('%H:%M')
#         temperature = row['temperature_2m']
#         precipitation_probability = row['precipitation_probability']
#         cloud_cover = cloud_percentage_to_emoji(row['cloud_cover'])
#         wind_speed_10m = row['wind_speed_10m']
#         wind_direction_10m = degrees_to_compass(row['wind_direction_10m'])
#
#         message = (f"    {time} {temperature}°C, ~{precipitation_probability}%💧, {cloud_cover}, "
#                    f"💨{wind_direction_10m} {wind_speed_10m}km/h")
#
#         # Check if the day has changed
#         if formatted_date != current_day:
#             current_day = formatted_date
#             formatted_data = (
#                 f"{swap_digits_with_emojis(formatted_date)}:\n{message}")
#         else:
#             formatted_data = message
#
#         hourly_data_formatted.append(formatted_data)
#
#     formatted_output = '\n'.join(hourly_data_formatted)
#
#     daily_dataframe = pd.DataFrame(data=daily_data)
#     daily_dataframe_rounded = daily_dataframe.map(lambda x: round(x, 2) if isinstance(x, (float, int)) else x)
#
#     # Print the rounded daily DataFrame as a formatted table
#     if days == 3:
#         return formatted_output

# test = give_table(27.938, 43.22, 3)
# print(test)
# bg = (43.22, 27.938)
# usa = (40.33, -74.02)
# weather_data = WeatherData(43.22, 27.938, 1)
# # print(weather_data.get_forecast())
# message = MessageCreator(weather_data.get_forecast(), 43.22, 27.938, 1)
# forecast = message.create_message()
#
# print(forecast)
import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry
from telegram_bot.Utils.get_local_time import get_local_time, get_timezone_difference


def timezone_difference(lat, lon):
    timezone_difference = get_timezone_difference(lat, lon)
    return timezone_difference


lat = 40.33
lon = -74.02
local_time = get_local_time(lat, lon)
current_hour = local_time.split(" ")[1].split(":")[0]

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": lat,
    "longitude": lon,
    "current": ["temperature_2m", "cloud_cover", "wind_speed_10m", "wind_direction_10m"],
    "hourly": ["temperature_2m", "precipitation_probability", "cloud_cover", "wind_speed_180m", "wind_direction_80m"],
    "daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_probability_max", "wind_speed_10m_max",
              "wind_direction_10m_dominant"],
    "timezone": "auto",
    "past_days": 1
}
responses = openmeteo.weather_api(url, params=params)

# Process first location. Add a for-loop for multiple locations or weather models
response = responses[0]
print(f"Coordinates {response.Latitude()}°E {response.Longitude()}°N")
print(f"Elevation {response.Elevation()} m asl")
print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

# Current values. The order of variables needs to be the same as requested.
current = response.Current()
current_temperature_2m = current.Variables(0).Value()
current_cloud_cover = current.Variables(1).Value()
current_wind_speed_10m = current.Variables(2).Value()
current_wind_direction_10m = current.Variables(3).Value()
#
# print(f"Current time {current.Time()}")
# print(f"Current temperature_2m {current_temperature_2m}")
# print(f"Current cloud_cover {current_cloud_cover}")
# print(f"Current wind_speed_10m {current_wind_speed_10m}")
# print(f"Current wind_direction_10m {current_wind_direction_10m}")

# Process hourly data. The order of variables needs to be the same as requested.
hourly = response.Hourly()
hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
hourly_precipitation_probability = hourly.Variables(1).ValuesAsNumpy()
hourly_cloud_cover = hourly.Variables(2).ValuesAsNumpy()
hourly_wind_speed_180m = hourly.Variables(3).ValuesAsNumpy()
hourly_wind_direction_80m = hourly.Variables(4).ValuesAsNumpy()

hourly_data = {"date": pd.date_range(
    start=pd.to_datetime(hourly.Time(), unit="s"),
    end=pd.to_datetime(hourly.TimeEnd(), unit="s"),
    freq=pd.Timedelta(seconds=hourly.Interval()),
    inclusive="left"
)}
hourly_data["temperature_2m"] = hourly_temperature_2m
hourly_data["precipitation_probability"] = hourly_precipitation_probability
hourly_data["cloud_cover"] = hourly_cloud_cover
hourly_data["wind_speed_180m"] = hourly_wind_speed_180m
hourly_data["wind_direction_80m"] = hourly_wind_direction_80m

hourly_dataframe = pd.DataFrame(data=hourly_data)
print(hourly_dataframe[int(current_hour) + 24 + timezone_difference(lat, lon)::4])
# print(hourly_dataframe)
# Process daily data. The order of variables needs to be the same as requested.
daily = response.Daily()
daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()
daily_temperature_2m_min = daily.Variables(1).ValuesAsNumpy()
daily_precipitation_probability_max = daily.Variables(2).ValuesAsNumpy()
daily_wind_speed_10m_max = daily.Variables(3).ValuesAsNumpy()
daily_wind_direction_10m_dominant = daily.Variables(4).ValuesAsNumpy()

daily_data = {"date": pd.date_range(
    start=pd.to_datetime(daily.Time(), unit="s"),
    end=pd.to_datetime(daily.TimeEnd(), unit="s"),
    freq=pd.Timedelta(seconds=daily.Interval()),
    inclusive="left"
)}
daily_data["temperature_2m_max"] = daily_temperature_2m_max
daily_data["temperature_2m_min"] = daily_temperature_2m_min
daily_data["precipitation_probability_max"] = daily_precipitation_probability_max
daily_data["wind_speed_10m_max"] = daily_wind_speed_10m_max
daily_data["wind_direction_10m_dominant"] = daily_wind_direction_10m_dominant

daily_dataframe = pd.DataFrame(data=daily_data)
print(timezone_difference(lat, lon))
print(daily_dataframe)
