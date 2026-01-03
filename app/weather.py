from pathlib import Path

from app.core.api.weather_api import get_weather
from app.core.history import save_weather, FileWeatherHistory, JsonWeatherHistory
from app.core.api.exceptions import CantGetCoordinates, GPS_COORDINATE_ERROR, API_WEATHER_ERROR
from app.core.api.exceptions import ApiServiceError
from app.core.api.gps_api import get_gps_coordinates

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
    print(weather.to_string())
    save_weather(weather,FileWeatherHistory(Path.cwd() / "weather_history.txt"))
    save_weather(weather,JsonWeatherHistory(Path.cwd() / "weather_history.json"))

if __name__ == '__main__':
    main()
