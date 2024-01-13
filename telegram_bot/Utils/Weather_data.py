import openmeteo_requests
import requests_cache
import pandas as pd
from datetime import datetime
from retry_requests import retry
from Utils.get_local_time import get_local_time, get_timezone_difference


class WeatherData:
    def __init__(self, lat, lon, days):
        self.__lat = lat
        self.__lon = lon
        self.__days = days
        self.__timezone_difference = self.__timezone_difference()
        self.__response = self.__get_response()

    def get_forecast(self):
        if self.__days == 3:
            forecast_kk = self.__forecast_for_three_days()
        elif self.__days == 10:
            forecast_kk = self.__forecast_for_ten_days()
        elif self.__days == 1:
            forecast_kk = self.__forecast_current()
        return forecast_kk

    def __timezone_difference(self):
        timezone_difference = get_timezone_difference(self.__lat, self.__lon)
        return timezone_difference

    def __get_response(self):
        cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
        retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
        openmeteo = openmeteo_requests.Client(session=retry_session)

        # Make sure all required weather variables are listed here
        # The order of variables in hourly or daily is important to assign them correctly below
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": self.__lat,
            "longitude": self.__lon,
            "current": ["temperature_2m", "cloud_cover", "wind_speed_10m", "wind_direction_10m"],
            "hourly": ["temperature_2m", "precipitation_probability", "cloud_cover", "wind_speed_10m",
                       "wind_direction_10m"],
            "daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_probability_max", "wind_speed_10m_max",
                      "wind_direction_10m_dominant"],
            "forecast_days": self.__days,
            "timezone": "auto",
            "past_days": 1

        }
        responses = openmeteo.weather_api(url, params=params)
        response = responses[0]
        # print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")

        return response

        # Process first location. Add a for-loop for multiple locations or weather models

    def __forecast_current(self):
        local_time = get_local_time(self.__lat, self.__lon)
        if not local_time:
            print("Не удалось определить часовой пояс для указанных координат.")
            return

        current = self.__response.Current()
        current_temperature_2m = current.Variables(0).Value()
        current_cloud_cover = current.Variables(1).Value()
        current_wind_speed_10m = current.Variables(2).Value()
        current_wind_direction_10m = current.Variables(3).Value()
        current_weather_dict = {
            "cur_temperature": round(current_temperature_2m, 0),
            "cur_cloud_cover": round(current_cloud_cover, 0),
            "cur_wind_speed": round(current_wind_speed_10m, 0),
            "cur_wind_direction": round(current_wind_direction_10m, 0),
        }
        return current_weather_dict

    def __forecast_for_three_days(self):

        # Process hourly data. The order of variables needs to be the same as requested.
        local_time = get_local_time(self.__lat, self.__lon)
        if not local_time:
            print("Не удалось определить часовой пояс для указанных координат.")
            return
        # print(local_time)

        current_hour = local_time.split(" ")[1].split(":")[0]
        # print(f"current_hour: {current_hour}")

        hourly = self.__response.Hourly()
        hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
        hourly_precipitation_probability = hourly.Variables(1).ValuesAsNumpy()
        hourly_cloud_cover = hourly.Variables(2).ValuesAsNumpy()
        hourly_wind_speed_10m = hourly.Variables(3).ValuesAsNumpy()
        hourly_wind_direction_10m = hourly.Variables(4).ValuesAsNumpy()

        hourly_data = {"date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s"),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s"),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left"
        )}
        hourly_data["temperature_2m"] = hourly_temperature_2m
        hourly_data["precipitation_probability"] = hourly_precipitation_probability
        hourly_data["cloud_cover"] = hourly_cloud_cover
        hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
        hourly_data["wind_direction_10m"] = hourly_wind_direction_10m
        hourly_dataframe = pd.DataFrame(data=hourly_data)
        hourly_dataframe_rounded = hourly_dataframe.map(lambda x: round(x, 0) if isinstance(x, (float, int)) else x)
        return hourly_dataframe_rounded[int(current_hour) + 24 + self.__timezone_difference::4]

    def __forecast_for_ten_days(self):
        # Process daily data. The order of variables needs to be the same as requested.
        daily = self.__response.Daily()
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
        daily_dataframe_rounded = daily_dataframe.map(lambda x: round(x, 0) if isinstance(x, (float, int)) else x)
        addition = 0
        if self.__timezone_difference > 0:
            addition += 1
        return daily_dataframe_rounded[1 + addition:11 + addition]

# forecast = WeatherData(43.22, 27.938, 3)
# finito = forecast.get_forecast()
# print(len(finito))

# print(forecast.tz)
# bg = (43.22, 27.938)
# la = (33.8, -118.3)
# usa = (40.33, -74.02)
