import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from aiogram.types import FSInputFile
import pandas as pd

class GraphicCreator:
    def __init__(self, dataframe_rounded, lat, lon, days):
        self.__lat = lat
        self.__lon = lon
        self.__days = days
        self.__dataframe_rounded = dataframe_rounded

    def create_graphic(self) -> FSInputFile:
        if self.__days == 3:
            self.__create_graphic_for_three_days()
        elif self.__days == 10:
            self.__create_graphic_for_ten_days()
        graphic = FSInputFile(f"Utils/graph{self.__days}.png")
        return graphic

    def __create_graphic_for_three_days(self, save_path="Utils/graph3.png"):
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
                     size=8, bbox=dict(facecolor='white', edgecolor='none', boxstyle='round4'))

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

        # Save the plot as an image
        plt.savefig(save_path)
        plt.close()

    def __create_graphic_for_ten_days(self, save_path="Utils/graph10.png"):
        df = self.__dataframe_rounded
        plt.figure(figsize=(10, 6))
        plt.plot(df['date'], df['temperature_2m_max'], label='Max Temperature', marker='o', color="red")
        plt.plot(df['date'], df['temperature_2m_min'], label='Min Temperature', marker='o', color="blue")

        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %d '))

        plt.title('10 days forecast')
        plt.ylabel('Temperature (°C)')
        plt.legend()
        plt.grid(True)
        plt.xticks(rotation=0)

        # Show the plot
        plt.tight_layout()
        plt.savefig(save_path)
        plt.close()
