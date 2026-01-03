import json
import ssl
import urllib
from datetime import datetime
from json import JSONDecodeError
from typing import Literal
from enum import Enum
from urllib.error import URLError

from app.core.api.gps_api import Coordinates
from app.core.api.exceptions import ApiServiceError
from app.core.api.weather_data import WeatherData, Celsius
from app.core.config import OPENWEATHER_URL

class WeatherType(Enum):
    THUNDERSTORM = "Гроза"
    DRIZZLE = "Изморось"
    RAIN = "Дождь"
    SNOW = "Снег"
    CLEAR = "Ясно"
    FOG = "Туман"
    CLOUDS = "Облачно"

def _get_openweather_response(latitude: float, longitude: float) -> str:
    ssl._create_default_https_context = ssl._create_unverified_context
    url = OPENWEATHER_URL.format(
        latitude=latitude, longitude=longitude)
    try:
        return urllib.request.urlopen(url).read()
    except URLError as e:
        raise ApiServiceError from e

def _parse_openweather_response(openweather_response: str,
                            datetime_weather: datetime,city:str) -> WeatherData:
    try:
        weather_json = json.loads(openweather_response)
    except JSONDecodeError as e:
        raise ApiServiceError from e
    return WeatherData(
        datetime_weather = datetime_weather,
        temperature=_parse_temperature(weather_json),
        humidity=_parse_humidity(weather_json),
        weather_type=_parse_weather_type(weather_json),
        sunrise_time=_parse_sun_time(weather_json, "sunrise"),
        sunset_time=_parse_sun_time(weather_json, "sunset"),
        place= _parse_name_place(weather_json),
        city= city,
        country = _parse_country(weather_json)
    )

def _parse_temperature(weather_json: dict) -> Celsius:
    return round(weather_json["main"]["temp"])

def _parse_humidity(weather_json: dict) -> Celsius:
    return round(weather_json["main"]["humidity"])

def _parse_weather_type(weather_json: dict) -> str:
    try:
        type_id = str(weather_json["weather"][0]["id"])
    except (IndexError, KeyError) as e:
        raise ApiServiceError from e
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

def _parse_name_place(weather_json: dict) -> str:
    return weather_json["name"]

def _parse_country(weather_json: dict) -> str:
    return weather_json["sys"]["country"]

def get_weather(coordinates: Coordinates) -> WeatherData:
    openweather_response = _get_openweather_response(
        longitude=coordinates.longitude, latitude=coordinates.latitude)
    return _parse_openweather_response(
        openweather_response, datetime.now(), coordinates.city
    )