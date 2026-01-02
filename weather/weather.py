from coordinates import get_gps_coordinates
from exceptions import CantGetCoordinates
from weather.exceptions import ApiServiceError
from weather_api import get_weather
from weather_printer import format_weather

def main():
    try:
        coordinates = get_gps_coordinates()
    except CantGetCoordinates:
        print("Не смог получить GPS-координаты")
        exit(1)
    try:
        weather = get_weather(coordinates)
    except ApiServiceError:
        print("Не смог получить погоду в API-сервиса погоды")
        exit(1)
    print(format_weather(weather))

if __name__ == '__main__':
    main()
