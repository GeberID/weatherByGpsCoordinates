from pathlib import Path

from app.core.history import save_weather, FileWeatherHistory
from app.core.api.exceptions import CantGetCoordinates, GPS_COORDINATE_ERROR, API_WEATHER_ERROR
from app.core.api.exceptions import ApiServiceError
from app.core.api.gps_api import get_gps_coordinates
from app.core.api.weather_api import get_weather
from app.core.weather_printer import format_weather


def main():
    try:
        coordinates = get_gps_coordinates()
    except CantGetCoordinates:
        print(GPS_COORDINATE_ERROR)
        exit(1)
    try:
        weather = get_weather(coordinates)
    except ApiServiceError:
        print(API_WEATHER_ERROR)
        exit(1)
    print(format_weather(weather))
    save_weather(weather,FileWeatherHistory(Path.cwd() / "weather_history.txt"))

if __name__ == '__main__':
    main()
