from app.core.api.weather_api import Weather

def format_weather(weather:Weather) -> str:
    return f'''
Температура = {weather.temperature}
Тип = {weather.weather_type}
Восход = {weather.sunrise_time}
Закат = {weather.sunrise_time}
Город = {weather.city}
Страна = {weather.country}'''
