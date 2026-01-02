from coordinates import get_gps_coordinates
from weather_api import get_weather
from weather_printer import format_weather

coordinates = get_gps_coordinates()
weather = get_weather(coordinates)

if __name__ == '__main__':
    print(format_weather(weather))
