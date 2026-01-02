import json
import ssl
import urllib
from dataclasses import dataclass
from datetime import datetime
from json import JSONDecodeError
from typing import TypeAlias, Literal
from enum import Enum
from urllib.error import URLError

from coordinates import Coordinates
from exceptions import ApiServiceError
from config import OPENWEATHER_URL

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

def _get_openweather_response(latitude: float, longitude: float) -> str:
    ssl._create_default_https_context = ssl._create_unverified_context
    url = OPENWEATHER_URL.format(
        latitude=latitude, longitude=longitude)
    try:
        return urllib.request.urlopen(url).read()
    except URLError:
        raise ApiServiceError

def _parse_openweather_response(openweather_response: str,
                                coordinates: Coordinates) -> Weather:
    try:
        weather_json = json.loads(openweather_response)
    except JSONDecodeError:
        raise ApiServiceError
    return Weather(
        temperature=_parse_temperature(weather_json),
        weather_type=_parse_weather_type(weather_json),
        sunrise_time=_parse_sun_time(weather_json, "sunrise"),
        sunset_time=_parse_sun_time(weather_json, "sunset"),
        city = coordinates.city,
        country = coordinates.country
    )

def _parse_temperature(weather_json: dict) -> Celsius:
    return round(weather_json["main"]["temp"])

def _parse_weather_type(weather_json: dict) -> WeatherType:
    try:
        type_id = str(weather_json["weather"][0]["id"])
    except (IndexError, KeyError):
        raise ApiServiceError
    weather_types = {
        "1": WeatherType.THUNDERSTORM.value,
        "3": WeatherType.DRIZZLE.value,
        "5": WeatherType.RAIN.value,
        "6": WeatherType.SNOW.value,
        "7": WeatherType.FOG.value,
        "800": WeatherType.CLEAR.value,
        "80": WeatherType.CLOUDS.value
    }
    for _id, _weather_type in weather_types.items():
        if type_id.startswith(_id):
            return _weather_type
    raise ApiServiceError

def _parse_sun_time(
        weather_json: dict,
        time: Literal["sunrise"] | Literal["sunset"]) -> datetime:
    return datetime.fromtimestamp(weather_json["sys"][time])

def get_weather(coordinates: Coordinates):
    openweather_response = _get_openweather_response(
        longitude=coordinates.longitude, latitude=coordinates.latitude)
    weather = _parse_openweather_response(openweather_response, coordinates)
    return weather