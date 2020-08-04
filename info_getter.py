import sys
import requests

def get_data():
    pass

def _main():
    city = sys.argv[1]
    data_name = sys.argv[2]

    APPID = "b6731c567cf35bb7de231f7ccaab085c"

    url = "http://api.openweathermap.org/data/2.5/{0}".format(data_name)
    data = requests.get(url, params={'q': city, 'lang': 'ru', 'units': 'metric', 'APPID': APPID}).text
    with open('{0}_fixture_{1}.txt'.format(data_name, city), 'w') as f:
        f.write(data)
    

if __name__ == '__main__':
    _main()
