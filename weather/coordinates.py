import json
from dataclasses import dataclass
from typing import Any
from urllib.request import urlopen

from exceptions import CantGetCoordinates

url = "http://ipinfo.io/json"


@dataclass(slots=True)
class Coordinates:
    latitude: float
    longitude: float
    city: str
    country: str

def _get_lat_lot(loc: list[str]) -> tuple[float, float]:
    latitude = loc.split(',')[0]
    longitude = loc.split(',')[1]
    return latitude,longitude

def get_gps_coordinates() -> Coordinates:
    urlopen(url)
    data = json.load(urlopen(url))
    if data is None:
        raise CantGetCoordinates(url)
    latitude, longitude = _get_lat_lot(data['loc'])
    city = data['city']
    country = data['country']
    return Coordinates(latitude = latitude, longitude = longitude, city = city, country = country)
