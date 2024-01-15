import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
import openmeteo_requests
import requests_cache
import seaborn as sns
from Utils.get_local_time import get_local_time

from .WindDirectoinReform import degrees_to_compass
from .cloud_percentage_to_emoji import cloud_percentage_to_emoji
from .swap_digits_with_emojis import swap_digits_with_emojis


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
        temperature_data = []
        precipitation_probability_data = []
        time_slots = []
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
        self.create_graphic()

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

    def create_graphic(self):
        df = self.__dataframe_rounded
        df['date'] = pd.to_datetime(df['date'])

        # Plotting using Matplotlib with line and circular markers
        plt.plot(df['date'], df['temperature_2m'], linestyle='-', marker='o', markersize=5, color='b')

        # Formatting the date ticks with hours and minutes vertically
        plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=4))
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

        # Set font size for hours and minutes using tick_params for both top and bottom
        plt.tick_params(axis='x', which='major', labelsize=7, bottom=True, top=True)

        plt.xticks(rotation='vertical')

        # Add a marker for a new day with day and month
        for _, day_date in df.groupby(df['date'].dt.date)['date']:
            plt.axvline(day_date.iloc[0], color='gray', linestyle='--', linewidth=0.5)
            plt.text(day_date.iloc[0], plt.ylim()[1] - 0.5, day_date.iloc[0].strftime('%b %d'),
                     ha='center', va='bottom', rotation=0, color='black',
                     size=9, bbox=dict(facecolor='white', edgecolor='none', boxstyle='round4'))

        # Set font size for the y-axis label
        plt.ylabel('Temperature (°C)', fontsize=10)

        # Adding title
        plt.title('Forecast for 3 days')

        # Display the grid inside the graph
        plt.grid(color='lightgray', linestyle='--', linewidth=0.5, which='both', axis='both', alpha=0.5)

        # Move the x-axis to the top
        plt.gca().xaxis.set_ticks_position('top')

        # Adding a legend
        plt.legend()

        # Display the plot
        plt.show()