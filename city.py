import requests
from requests.exceptions import HTTPError
import time
import os
import json
from googletrans import Translator
import numpu
class OpenWeatherApi:

    __APPID = "b6731c567cf35bb7de231f7ccaab085c"
    __timers = {'forecast': 60 * 60 * 2,
                'weather': 60 * 10
                }

    def __init__(self, connection=True):
        self.translator = Translator()

    def _dump(self, data, data_name, city):
        with open('{0}_fixture_{1}_time.txt'.format(data_name, city), 'w') as f:
            print(time.time())
            f.write(str(time.time()))
        with open('{0}_fixture_{1}.txt'.format(data_name, city), 'w') as f:
            json.dump(data, f)

    def _load_data(self, data_name, city) -> dict:
        with open('{0}_fixture_{1}.txt'.format(data_name, city), 'r') as f:
            return json.load(f)

    def _load_time(self, data_name, city):
        with open('{0}_fixture_{1}_time.txt'.format(data_name, city), 'r') as f:
            return float(f.read())

    def get_raw_data(self, data_name, city) -> dict:
        file_path = './{0}_fixture_{1}.txt'.format(data_name, city)
        if os.path.exists(file_path):
            t = self._load_time(data_name, city)
            if time.time() - t < self.__timers[data_name]:
                return self._load_data(data_name, city)

        url = "http://api.openweathermap.org/data/2.5/{0}".format(data_name)
        response = requests.get(url, params={'q': city, 'lang': 'ru', 'units': 'metric', 'APPID': self.__APPID})
        try:
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
            return None
        except Exception as err:
            print(f'Other error occurred: {err}')
            return None
        else:
            data = response.json()
            self._dump(data, data_name, city)
            return response.json()

    def get_weather(self, city):
        data = self.get_raw_data('weather', self.translator.translate(city, dest='en').text)
        if data == None:
            return 'Got problems on server'
        answer = 'Погода в {0}\n' \
                 'Температура {1} С°\n' \
                 'Ощущается как {2} С°\n' \
                 'Относительная влажность {3}%\n' \
                 'Скорость ветра {4} м/c\n' \
                 '{5}\n'.format(data['name'],
                            data['main']['temp'],
                            data['main']['feels_like'],
                            data['main']['humidity'],
                            data['wind']['speed'],
                            data['weather'][0]['description'].capitalize()
                            )
        return answer

    def get_forecast(self, city):
        data = self.get_raw_data('forecast', self.translator.translate(city, dest='en').text)
        if data == None:
            return 'Got problems on server'
        n = 3
        answer = 'Прогноз погоды в {0} на ближайшие несколько часов:'.format(data['city']['name'], n * 3)
        for i in range(1, n+1):
            dl = data['list'][i]
            answer += '\nОжидается на {0}:\n' \
                      'Температура {1} С°\n' \
                      'Ощущается как {2} С°\n' \
                      'Относительная влажность {3}%\n' \
                      'Скорость ветра {4} м/c\n' \
                      '{5}\n'.format(dl['dt_txt'],
                                   dl['main']['temp'],
                                   dl['main']['feels_like'],
                                   dl['main']['humidity'],
                                   dl['wind']['speed'],
                                   dl['weather'][0]['description'].capitalize()
                                   )
        return answer

##################################################################################

def main():
    weather_api = OpenWeatherApi()
    print(weather_api.get_weather('Moscow'))
    print(weather_api.get_forecast('Moscow'))

if __name__ == '__main__':
    main()
