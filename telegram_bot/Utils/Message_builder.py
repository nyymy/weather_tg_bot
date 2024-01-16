from Utils.Weather_data import WeatherData
from Utils.Message_creator import MessageCreator
from Utils.Graphic_creator import GraphicCreator


class MessageBuilder:
    def __init__(self, lat, lon, days):
        self.__lat = lat
        self.__lon = lon
        self.__days = days
        self.__dataframe_rounded = self.__get_dataframe()


    def __get_dataframe(self):
        weather_data = WeatherData(lat=self.__lat, lon=self.__lon, days=self.__days)
        dataframe_rounded = weather_data.get_forecast()
        return dataframe_rounded

    def create_message_text(self):
        forecast = MessageCreator(dataframe_rounded=self.__dataframe_rounded, lat=self.__lat, lon=self.__lon,
                                  days=self.__days)
        text_message = forecast.create_message()
        return text_message

    def create_image(self):
        graph_builder = GraphicCreator(dataframe_rounded=self.__dataframe_rounded, lat=self.__lat, lon=self.__lon,
                                       days=self.__days)
        graph = graph_builder.create_graphic()
        return graph
