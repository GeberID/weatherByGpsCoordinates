from datetime import datetime
from pathlib import Path
from typing import Protocol

from app.core.api.weather_api import Weather
from app.core.weather_printer import format_weather


class WeatherHistory(Protocol):
    def save(self, weather: Weather) -> None:
        raise NotImplementedError

class FileWeatherHistory:
    def __init__(self, file: Path) -> None:
        self._file = file

    def save(self, weather: Weather) -> None:
        date_now = datetime.now()
        formatted_weather = format_weather(weather)
        with open(self._file, 'a') as file:
            file.write(f"{date_now.strftime('%Y-%m-%d %H:%M:%S')}, {formatted_weather}\n\n")

def save_weather(weather: Weather, storage: WeatherHistory) -> None:
    storage.save(weather)
