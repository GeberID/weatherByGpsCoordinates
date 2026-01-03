import json
from datetime import datetime
from pathlib import Path
from typing import Protocol, TypedDict
from app.core.api.weather_api import WeatherData

class WeatherHistory(Protocol):
    def save(self, weather: WeatherData) -> None:
        raise NotImplementedError

class JsonHistoryData(TypedDict):
    date: str
    weather: dict[str,str]

class FileWeatherHistory:
    def __init__(self, file: Path) -> None:
        self._file = file

    def save(self, weather: WeatherData) -> None:
        formatted_weather = weather.to_string()
        with open(self._file, 'a') as file:
            file.write(f"{formatted_weather}\n\n")

class JsonWeatherHistory(WeatherHistory):
    def __init__(self, json_file: Path) -> None:
        self._json_file = json_file
        self._init_storage()

    def save(self, weather: WeatherData) -> None:
        history = self._read_json()
        history.append({
            'date': weather.datetime_weather.strftime('%Y-%m-%d %H:%M:%S'),
            'weather': weather.to_json_str()
        })
        self._write_json(history)

    def _init_storage(self) -> None:
        if not self._json_file.exists():
            self._json_file.write_text('[]', encoding='utf-8')

    def _read_json(self) -> list[JsonHistoryData]:
        with open(self._json_file, 'r') as file:
            return json.load(file)

    def _write_json(self, history: list[JsonHistoryData]) -> None:
        with open(self._json_file, 'w') as file:
            json.dump(history, file, ensure_ascii=False, indent=4)


def save_weather(weather: WeatherData, storage: WeatherHistory) -> None:
    storage.save(weather)
