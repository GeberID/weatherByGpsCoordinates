from pathlib import Path

from coordinates import get_gps_coordinates
from exceptions import CantGetCoordinates, GPS_COORDINATE_ERROR, API_WEATHER_ERROR
from exceptions import ApiServiceError
from history import save_weather, FileWeatherHistory
from weather_api import get_weather
from weather_printer import format_weather

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
