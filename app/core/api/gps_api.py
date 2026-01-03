import json
from dataclasses import dataclass
from urllib.request import urlopen

from app.core.api.exceptions import CantGetCoordinates
from app.core.config import COORDINATE


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
    urlopen(COORDINATE)
    data = json.load(urlopen(COORDINATE))
    if data is None:
        raise CantGetCoordinates(COORDINATE)
    latitude, longitude = _get_lat_lot(data['loc'])
    city = data['city']
    country = data['country']
    return Coordinates(latitude = latitude, longitude = longitude, city = city, country = country)
