from dataclasses import dataclass
from datetime import datetime
from typing import TypeAlias
from enum import Enum
from coordinates import Coordinates

Celsius : TypeAlias = float


class WeatherType(Enum):
    THUNDERSTORM = "Гроза"
    DRIZZLE = "Изморось"
    RAIN = "Дождь"
    SNOW = "Снег"
    CLEAR = "Ясно"
    FOG = "Туман"
    CLOUDS = "Облачно"

@dataclass
class Weather:
    temperature: Celsius
    weather_type: WeatherType
    sunrise_time: datetime
    sunset_time: datetime
    city: str
    country: str

def get_weather(coordinates: Coordinates):
    return Weather(temperature=20,
                   weather_type=WeatherType.CLEAR,
                   sunset_time= datetime.fromisoformat("2022-05-04 04:00:00"),
                   sunrise_time=datetime.fromisoformat("2022-05-04 20:25:00"),
                   city = coordinates.city,
                   country = coordinates.country)