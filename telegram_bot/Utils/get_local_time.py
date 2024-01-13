from timezonefinder import TimezoneFinder
from datetime import datetime
import pytz
from datetime import datetime, timedelta


class LocalTime:
    def __init__(self, latitude, longitude, start_hour, end_hour):
        self.start_hour = start_hour
        self.end_hour = end_hour
        self.latitude = latitude
        self.longitude = longitude
        self.local_time = self.get_local_time()
        self.hour_difference_with_UTC = self.calculate_hour_difference()

    def calculate_hour_difference(self):
        # Предположим, что start_hour и end_hour представляют собой целые числа часов
        start_time = datetime.strptime(str(self.start_hour), "%H")
        end_time = datetime.strptime(str(self.end_hour), "%H")

        # Вычисляем разницу во времени
        time_difference = end_time - start_time

        # Преобразуем разницу в часы
        hours_difference = time_difference.total_seconds() / 3600

        return hours_difference

    def get_local_time(self):
        # Используем TimezoneFinder для определения часового пояса по координатам
        tz_finder = TimezoneFinder()
        timezone_str = tz_finder.timezone_at(lat=self.latitude, lng=self.longitude)

        if timezone_str:
            # Получаем объект часового пояса
            timezone = pytz.timezone(timezone_str)

            # Получаем текущее время в указанном часовом поясе
            local_time = datetime.now(timezone)

            return local_time.strftime("%Y-%m-%d %H:%M:%S %Z")
        else:
            return "Не удалось определить часовой пояс для указанных координат."

    def get_timezone_difference(self):
        tz_finder = TimezoneFinder()
        timezone_str = tz_finder.timezone_at(lat=self.latitude, lng=self.longitude)

        if timezone_str:
            # Получаем объект часового пояса с использованием pytz
            tz = pytz.timezone(timezone_str)
            now = datetime.now(tz)
            offset_seconds = now.utcoffset().total_seconds()

            # Преобразуем секунды в часы
            offset_hours = offset_seconds / 3600

            return int(offset_hours)
        else:
            pass


def get_local_time(latitude, longitude):
    # Используем TimezoneFinder для определения часового пояса по координатам
    tz_finder = TimezoneFinder()
    timezone_str = tz_finder.timezone_at(lat=latitude, lng=longitude)

    if not timezone_str:
        return None

    # Получаем объект часового пояса
    timezone = pytz.timezone(timezone_str)

    # Получаем текущее время в указанном часовом поясе
    local_time = datetime.now(timezone)

    return local_time.strftime("%Y-%m-%d %H:%M:%S %Z")


def get_timezone_difference(lat, lng):
    tz_finder = TimezoneFinder()
    timezone_str = tz_finder.timezone_at(lat=lat, lng=lng)

    # Получаем объект часового пояса с использованием pytz
    tz = pytz.timezone(timezone_str)
    now = datetime.now(tz)
    offset_seconds = now.utcoffset().total_seconds()

    # Преобразуем секунды в часы
    offset_hours = offset_seconds / 3600

    return int(offset_hours)
# time = get_timezone_difference(40.33, -74.02)
# print(time)
