class CantGetCoordinates(Exception):
    def __init__(self, url):
        self.url = url

    def __str__(self):
        return f"Данные координат не получены c url {self.url}"

class ApiServiceError(Exception):
    def __init__(self, request, response):
        self.request = request
        self.response = response
    def __str__(self):
        return (f"Ошибка запроса погоды {self.request}"
                f"Ответ {self.response}")

GPS_COORDINATE_ERROR = "Не смог получить GPS-координаты"
API_WEATHER_ERROR = "Не смог получить погоду в API-сервиса погоды"