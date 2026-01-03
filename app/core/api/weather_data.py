from dataclasses import dataclass
from datetime import datetime
from typing import TypeAlias

Celsius : TypeAlias = float
@dataclass
class WeatherData:
    datetime_weather: datetime
    temperature: Celsius
    humidity: float
    weather_type: str
    sunrise_time: datetime
    sunset_time: datetime
    place: str
    city: str
    country: str

    def to_string(self) -> str:
        return (
f'''
Время = {self.datetime_weather.strftime('%Y-%m-%d %H:%M:%S')}
Температура = {self.temperature}
Влажность = {self.humidity}
Тип = {self.weather_type}
Восход = {self.sunrise_time}
Закат = {self.sunset_time}
Место = {self.place}
Город = {self.city}
Страна = {self.country}''')

    def to_json_str(self) -> dict[str,str]:
        return {"Время":self.datetime_weather.strftime('%Y-%m-%d %H:%M:%S'),
                "Температура":self.temperature,
                "Влажность":self.humidity,
                "Тип":self.weather_type,
                "Восход":self.sunrise_time.strftime('%Y-%m-%d %H:%M:%S'),
                "Закат":self.sunset_time.strftime('%Y-%m-%d %H:%M:%S'),
                "Место":self.place,
                "Город":self.city,
                "Страна":self.country,}
