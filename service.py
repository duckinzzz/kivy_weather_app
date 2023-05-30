from time import sleep
from datetime import datetime
import requests
from plyer import notification

from jnius import autoclass
PythonService = autoclass('org.kivy.android.PythonService')
PythonService.mService.setAutoRestartService(True)

api_key = "API_KEY"
while True:
    now = datetime.now().strftime("%H:%M")
    if now == '18:00':
        x = list(map(float, open('coords.txt').read().split()))
        coordinates = {'lon': x[1], 'lat': x[0]}
        print(coordinates)
        print('получаю прогноз...')
        url = f"https://api.openweathermap.org/data/2.5/forecast?" \
              f"lat={coordinates['lat']}&lon={coordinates['lon']}&appid={api_key}&units=metric"
        response = requests.get(url)
        x = response.json()
        print('получил прогноз:\n', x)
        forecast_info = []
        i = 0
        while i < 40:
            cur_date = x['list'][i]['dt_txt'].split()[0]
            cur_max = 0.
            cur_max_index = 0
            will_rain = 'none'
            while i < 40 and x['list'][i]['dt_txt'].split()[0] == cur_date:
                if cur_max < x['list'][i]['main']['temp']:
                    cur_max = x['list'][i]['main']['temp']
                    cur_max_index = i
                if 200 <= x['list'][i]['weather'][0]['id'] <= 232:
                    will_rain = 'storm'
                elif 300 <= x['list'][i]['weather'][0]['id'] <= 321 or 500 <= x['list'][i]['weather'][0]['id'] <= 531:
                    will_rain = 'rain'
                elif 600 <= x['list'][i]['weather'][0]['id'] <= 622:
                    will_rain = 'snow'
                i += 1
            forecast_info.append([cur_max_index, will_rain])
        for m in forecast_info:
            i = m[0]
            temp = x['list'][i]['main']['temp']
            daytime = x['list'][i]['sys']['pod']
            date = x['list'][i]['dt_txt'].split()[0]
            print(*m, temp, daytime, date)

        if forecast_info[1][1] == 'rain':
            notification.notify(title='It might rain tomorrow',
                                message="Don't forget your umbrella!", ticker='Forecast', app_icon='assets/rain.png')
        elif forecast_info[1][1] == 'snow':
            notification.notify(title='It might snow tomorrow',
                                message="Don't forget to wear a hat!", ticker='Forecast', app_icon='assets/snow.png')
        sleep(10)
