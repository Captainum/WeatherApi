import json

from unittest.mock import patch

from city import OpenWeatherApi
from city import CityInfo

class OpenWeatherApi_Tester():
    def __init__(self):
        self.Moscow = CityInfo('Moscow')

    def mocked_get_weather(self):
        with open('weather_fixture,txt') as f:
            return json.loads(f.read())

    def mocked_get_forecast(self):
        with open('forecast_fixture.txt') as f:
            return json.loads(f.read())

    @patch('city.OpenWeatherApi.get_weather', mocked_get_weather)

    def test_get_weather(self):
        print(
