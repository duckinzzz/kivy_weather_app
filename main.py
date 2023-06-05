import requests
from kivy.core.text import LabelBase
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from plyer import gps
from kivy.utils import platform
from kivy.clock import mainthread
from kivy.properties import StringProperty
from kivy.clock import Clock

Window.size = (338, 600)
Window.keyboard_anim_args = {'d': .2, 't': 'in_out_expo'}
Window.softinput_mode = "below_target"
api_key = "API_KEY"

kv = '''
MDFloatLayout:
    md_bg_color: 1, 1, 1, 1

    Image:
        source: "assets/location.png"
        size_hint: .1, .1
        pos_hint: {"center_x": .5, "center_y": .95}

    Button:
        size_hint: .1, .1
        pos_hint: {"center_x": .9, "center_y": .95}
        background_color: 1,1,1,0
        on_release: app.gps_location_weather()
    Image:
        source: "assets/get_location.png"
        size_hint: .1, .1
        pos_hint: {"center_x": .9, "center_y": .95}

    MDLabel:
        id: location
        text: ""
        pos_hint: {"center_x": .5, "center_y": .89  }
        halign: "center"
        font_size:  "20sp"
        font_name: "BPoppins"
    Image:
        id: weather_image
        source: "assets/partlyclouds.png"
        pos_hint: {"center_x": .5, "center_y": .77}
    MDLabel:
        id: temperature
        text: ""
        markup: True
        pos_hint: {"center_x": .5, "center_y": .62}
        halign: "center"
        font_size:  "60sp"
    MDLabel:
        id: weather
        text: ""
        markup: True
        pos_hint: {"center_x": .5, "center_y": .54}
        halign: "center"
        font_size:  "20sp"
        font_name: "Poppins"

    MDFloatLayout:
        pos_hint: {"center_x": .25, "center_y": .45}
        size_hint: .22, .1
        Image:
            source: "assets/humidity.png"
            pos_hint: {"center_x": .1, "center_y": .5}
        MDLabel:
            id: humidity
            text: "  %"
            pos_hint: {"center_x": 1, "center_y": .7}
            font_size:  "18sp"
            font_name: "Poppins"
        MDLabel:
            text: "Humidity"
            pos_hint: {"center_x": 1, "center_y": .3}
            font_size:  "14sp"
            font_name: "Poppins"    

    MDFloatLayout:
        pos_hint: {"center_x": .7, "center_y": .45}
        size_hint: .22, .1
        Image:
            source: "assets/wind.png"
            pos_hint: {"center_x": .1, "center_y": .5}

        MDLabel:
            id: wind_speed
            text: "   m/s"
            pos_hint: {"center_x": 1.1, "center_y": .7}
            font_size:  "18sp"
            font_name: "Poppins"
        MDLabel:
            text: "Wind"
            pos_hint: {"center_x": 1.1, "center_y": .3}
            font_size:  "14sp"
            font_name: "Poppins"

    MDFloatLayout:
        size_hint_y: .12
        canvas:
            Color:
                rgb: rgba(121, 86, 162) # цвет фона нижней панели
            RoundedRectangle:
                size: self.size
                pos: self.pos
                radius: [30,30,0,0]

        MDFloatLayout:
            pos_hint: {"center_x": .38, "center_y": .5}
            size_hint: .7, .7
            canvas:
                Color:
                    rgb: rgba(181, 159, 242) # цвет кнопки
                RoundedRectangle:
                    size: self.size
                    pos: self.pos
                    radius: [15]
            TextInput:
                id: city_name
                hint_text: "Enter city name"
                size_hint: 1, None
                pos_hint: {"center_x": .5, "center_y": .5}
                height: self.minimum_height
                multiline: False
                font_name: "BPoppins"
                font_size: "20sp"
                hint_text_color: 1,1,1,1
                foreground_color: 1,1,1,1
                background_color: 1,1,1,0
                padding: 15
                halign: "center"
                cursor_color: 1,1,1,1
                cursor_width: "2sp"

        Button:
            id: get_weather_button
            # text: "G"
            font_name: "BPoppins"
            font_size: "20sp"
            size_hint: .2, .7
            pos_hint: {"center_x": .87, "center_y": .5}
            background_color: 1,1,1,0
            color: rgba(148, 117, 255, 255)
            on_release: app.search_weather()
            canvas.before:
                Color:
                    rgb: 1,1,1,1
                RoundedRectangle:
                    size: self.size
                    pos: self.pos
                    radius: [15]
        Image:
            source: "assets/search_icon.png"
            size_hint: .3, .3
            pos_hint: {"center_x": .87, "center_y": .5}

    MDFloatLayout:
        pos_hint: {"center_x": .5, "center_y": .25}
        size_hint: .9, .2
        canvas:
            Color:
                rgb: rgba(133, 95, 185)
            RoundedRectangle:
                size: self.size
                pos: self.pos
                radius: [40,40,40,40]

        MDFloatLayout:
            pos_hint: {"center_x": .11, "center_y": .5}
            size_hint: .17, .9
            canvas:
                Color:
                    rgb: rgba(255,255,255)
                RoundedRectangle:
                    size: self.size
                    pos: self.pos
                    radius: [25,25,25,25]

            MDLabel:
                id: d1_date
                text: "01"
                pos_hint: {"center_x": 0.5, "center_y": .875}
                halign: "center"
                font_size:  "15sp"
                font_name: "Poppins"
            MDLabel:
                id: d1_temp
                text: "15°"
                pos_hint: {"center_x": 0.5, "center_y": .2}
                halign: "center"
                font_size:  "18sp"
                font_name: "Poppins"
            Image:
                id: d1_img
                source: "assets/sun.png"
                pos_hint: {"center_x": .5, "center_y": .5}
                size_hint: .9,.9

        MDFloatLayout:
            pos_hint: {"center_x": .305, "center_y": .5}
            size_hint: .17, .9
            canvas:
                Color:
                    rgb: rgba(255,255,255)
                RoundedRectangle:
                    size: self.size
                    pos: self.pos
                    radius: [25,25,25,25]
            MDLabel:
                id: d2_date
                text: "02"
                pos_hint: {"center_x": 0.5, "center_y": .875}
                halign: "center"
                font_size:  "15sp"
                font_name: "Poppins"        
            MDLabel:
                id: d2_temp
                text: "15°"
                pos_hint: {"center_x": 0.5, "center_y": .2}
                halign: "center"
                font_size:  "18sp"
                font_name: "Poppins"
            Image:
                id: d2_img
                source: "assets/snow.png"
                pos_hint: {"center_x": .5, "center_y": .5}
                size_hint: .9,.9        

        MDFloatLayout:
            pos_hint: {"center_x": .5, "center_y": .5}
            size_hint: .17, .9
            canvas:
                Color:
                    rgb: rgba(255,255,255)
                RoundedRectangle:
                    size: self.size
                    pos: self.pos
                    radius: [25,25,25,25]
            MDLabel:
                id: d3_date
                text: "03"
                pos_hint: {"center_x": 0.5, "center_y": .875}
                halign: "center"
                font_size:  "15sp"
                font_name: "Poppins"
            MDLabel:
                id: d3_temp
                text: "15°"
                pos_hint: {"center_x": 0.5, "center_y": .2}
                halign: "center"
                font_size:  "18sp"
                font_name: "Poppins"
            Image:
                id: d3_img
                source: "assets/wind.png"
                pos_hint: {"center_x": .5, "center_y": .5}
                size_hint: .9,.9        

        MDFloatLayout:
            pos_hint: {"center_x": .695, "center_y": .5}
            size_hint: .17, .9
            canvas:
                Color:
                    rgb: rgba(255,255,255)
                RoundedRectangle:
                    size: self.size
                    pos: self.pos
                    radius: [25,25,25,25]
            MDLabel:
                id: d4_date
                text: "04"
                pos_hint: {"center_x": 0.5, "center_y": .875}
                halign: "center"
                font_size:  "15sp"
                font_name: "Poppins"        
            MDLabel:
                id: d4_temp
                text: "15°"
                pos_hint: {"center_x": 0.5, "center_y": .2}
                halign: "center"
                font_size:  "18sp"
                font_name: "Poppins"
            Image:
                id: d4_img
                source: "assets/storm.png"
                pos_hint: {"center_x": .5, "center_y": .5}
                size_hint: .9,.9        
        MDFloatLayout:
            pos_hint: {"center_x": .89, "center_y": .5}
            size_hint: .17, .9
            canvas:
                Color:
                    rgb: rgba(255,255,255)
                RoundedRectangle:
                    size: self.size
                    pos: self.pos
                    radius: [25,25,25,25]
            MDLabel:
                id: d5_date
                text: "05"
                pos_hint: {"center_x": 0.5, "center_y": .875}
                halign: "center"
                font_size:  "15sp"
                font_name: "Poppins"   
            MDLabel:
                id: d5_temp
                text: "15°"
                pos_hint: {"center_x": 0.5, "center_y": .2}
                halign: "center"
                font_size:  "18sp"
                font_name: "Poppins"
            Image:
                id: d5_img
                source: "assets/haze.png"
                pos_hint: {"center_x": .5, "center_y": .5}
                size_hint: .9,.9
'''


class WeatherApp(MDApp):
    gps_city_memory = ''
    last_call_coord = {'lon': 0., 'lat': 0.}

    gps_location = StringProperty()
    gps_status = StringProperty('=)')

    def forecast_display_clear(self):
        self.root.ids.d1_img.source = "assets/no_data.png"
        self.root.ids.d1_temp.text = '-°'
        self.root.ids.d2_img.source = "assets/no_data.png"
        self.root.ids.d2_temp.text = '-°'
        self.root.ids.d3_img.source = "assets/no_data.png"
        self.root.ids.d3_temp.text = '-°'
        self.root.ids.d4_img.source = "assets/no_data.png"
        self.root.ids.d4_temp.text = '-°'
        self.root.ids.d5_img.source = "assets/no_data.png"
        self.root.ids.d5_temp.text = '-°'

    def no_connection(self):
        self.root.ids.temperature.text = "[b]--[/b]°"
        self.root.ids.weather.text = "No connection"
        self.root.ids.humidity.text = "--%"
        self.root.ids.wind_speed.text = "-- m/s"
        self.root.ids.location.text = ""
        self.root.ids.weather_image.source = "assets/notconnected.png"
        self.forecast_display_clear()

    def city_notfound(self):
        self.root.ids.temperature.text = "[b]--[/b]°"
        self.root.ids.weather.text = "City Not Found"
        self.root.ids.humidity.text = "--%"
        self.root.ids.wind_speed.text = "-- m/s"
        self.root.ids.location.text = ""
        self.root.ids.weather_image.source = "assets/notfound.png"
        self.forecast_display_clear()

    def waiting_for_gps(self):
        self.root.ids.temperature.text = "[b]--[/b]°"
        self.root.ids.weather.text = "Waiting for GPS..."
        self.root.ids.humidity.text = "--%"
        self.root.ids.wind_speed.text = "-- m/s"
        self.root.ids.location.text = ""
        self.root.ids.weather_image.source = "assets/waiting_for_gps.png"
        self.forecast_display_clear()

    def gps_not_allowed(self):
        self.root.ids.temperature.text = "[b]--[/b]°"
        self.root.ids.weather.text = "GPS was not allowed"
        self.root.ids.humidity.text = "--%"
        self.root.ids.wind_speed.text = "-- m/s"
        self.root.ids.location.text = ""
        self.root.ids.weather_image.source = "assets/gps_not_allowed.png"
        self.forecast_display_clear()

    def gps_failed(self):
        self.root.ids.temperature.text = "[b]--[/b]°"
        self.root.ids.weather.text = "GPS fail, retrying..."
        self.root.ids.humidity.text = "--%"
        self.root.ids.wind_speed.text = "-- m/s"
        self.root.ids.location.text = ""
        self.root.ids.weather_image.source = "assets/gps_not_allowed.png"
        self.forecast_display_clear()

    def gps_location_weather(self):
        print('finding on: ', self.last_call_coord)
        self.get_weather(self.last_call_coord)

    def get_weather(self, coordinates):
        if coordinates != {'lon': 0., 'lat': 0.}:
            try:
                print('getting weather...')
                url = f"https://api.openweathermap.org/data/2.5/weather?" \
                      f"lat={coordinates['lat']}&lon={coordinates['lon']}&appid={api_key}&units=metric"
                response = requests.get(url)
                x = response.json()
                print('got result\n', x)
                if x["cod"] != "404":
                    self.root.ids.city_name.text = ''
                    temperature = round(x['main']['temp'])
                    humidity = x['main']['humidity']
                    weather = x['weather'][0]['main']
                    weather_id = str(x['weather'][0]['id'])
                    wind_speed = round(x['wind']['speed'])
                    location = x["name"] + ', ' + x['sys']['country']
                    self.root.ids.temperature.text = f"[b]{temperature}[/b]°"
                    self.root.ids.weather.text = str(weather)
                    self.root.ids.humidity.text = f"{humidity}%"
                    self.root.ids.wind_speed.text = f"{wind_speed} m/s"
                    self.root.ids.location.text = location
                    if weather_id == '800':
                        self.root.ids.weather_image.source = "assets/sun.png"
                    elif '200' <= weather_id <= '232':
                        self.root.ids.weather_image.source = "assets/storm.png"
                    elif '300' <= weather_id <= '321' or '500' <= weather_id <= '531':
                        self.root.ids.weather_image.source = "assets/rain.png"
                    elif '600' <= weather_id <= '622':
                        self.root.ids.weather_image.source = "assets/snow.png"
                    elif '701' <= weather_id <= '781':
                        self.root.ids.weather_image.source = "assets/haze.png"
                    elif '801' <= weather_id <= '804':
                        self.root.ids.weather_image.source = "assets/clouds.png"
                    self.forecast(coordinates)
                else:
                    self.city_notfound()
                    print("city not found")
            except requests.ConnectionError:
                self.no_connection()
                print("no connection")
        else:
            self.gps_failed()
            print('gps retrying')
            Clock.schedule_once(lambda dt: self.get_weather(self.last_call_coord), 1)

    def search_weather(self):
        city_name = self.root.ids.city_name.text
        if city_name != '':
            print('getting geocode...')
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
            response = requests.get(url)
            x = response.json()
            if x['cod'] == 200:
                print('got result:\n', x['coord'])
                coorditanes = x['coord']
                self.get_weather(coorditanes)
            else:
                self.city_notfound()

    def forecast(self, coordinates):
        print('getting forecast...')
        url = f"https://api.openweathermap.org/data/2.5/forecast?" \
              f"lat={coordinates['lat']}&lon={coordinates['lon']}&appid={api_key}&units=metric"
        response = requests.get(url)
        x = response.json()
        print('got forecast:\n', x)
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

        def choose_img(weather_id):
            if weather_id == '800':
                return "assets/sun.png"
            elif '200' <= weather_id <= '232':
                return "assets/storm.png"
            elif '300' <= weather_id <= '321' or '500' <= weather_id <= '531':
                return "assets/rain.png"
            elif '600' <= weather_id <= '622':
                return "assets/snow.png"
            elif '701' <= weather_id <= '781':
                return "assets/haze.png"
            elif '801' <= weather_id <= '804':
                return "assets/clouds.png"

        self.root.ids.d1_img.source = choose_img(str(x["list"][forecast_info[0][0]]['weather'][0]['id']))
        self.root.ids.d1_temp.text = str(round(x['list'][forecast_info[0][0]]['main']['temp'])) + '°'
        self.root.ids.d1_date.text = x["list"][forecast_info[0][0]]['dt_txt'].split()[0].split('-')[2]

        self.root.ids.d2_img.source = choose_img(str(x["list"][forecast_info[1][0]]['weather'][0]['id']))
        self.root.ids.d2_temp.text = str(round(x['list'][forecast_info[1][0]]['main']['temp'])) + '°'
        self.root.ids.d2_date.text = x["list"][forecast_info[1][0]]['dt_txt'].split()[0].split('-')[2]

        self.root.ids.d3_img.source = choose_img(str(x["list"][forecast_info[2][0]]['weather'][0]['id']))
        self.root.ids.d3_temp.text = str(round(x['list'][forecast_info[2][0]]['main']['temp'])) + '°'
        self.root.ids.d3_date.text = x["list"][forecast_info[2][0]]['dt_txt'].split()[0].split('-')[2]

        self.root.ids.d4_img.source = choose_img(str(x["list"][forecast_info[3][0]]['weather'][0]['id']))
        self.root.ids.d4_temp.text = str(round(x['list'][forecast_info[3][0]]['main']['temp'])) + '°'
        self.root.ids.d4_date.text = x["list"][forecast_info[3][0]]['dt_txt'].split()[0].split('-')[2]

        self.root.ids.d5_img.source = choose_img(str(x["list"][forecast_info[4][0]]['weather'][0]['id']))
        self.root.ids.d5_temp.text = str(round(x['list'][forecast_info[4][0]]['main']['temp'])) + '°'
        self.root.ids.d5_date.text = x["list"][forecast_info[4][0]]['dt_txt'].split()[0].split('-')[2]

    def start_service(self):
        from jnius import autoclass
        service = autoclass('org.duckinzzz.kivyweather.ServiceNotify')
        mActivity = autoclass('org.kivy.android.PythonActivity').mActivity
        argument = ''
        service.start(mActivity, argument)

    def request_android_permissions(self):
        from android.permissions import request_permissions, Permission

        def callback(permissions, results):
            if all([res for res in results]):
                print("callback. All permissions granted.")
                self.gps_start(1000, 0)
                Clock.schedule_once(lambda dt: self.get_weather(self.last_call_coord), 5)
            else:
                print("callback. Some permissions refused.")
                self.gps_not_allowed()

        request_permissions([Permission.ACCESS_COARSE_LOCATION,
                             Permission.ACCESS_FINE_LOCATION,
                             Permission.FOREGROUND_SERVICE], callback)

    def gps_start(self, minTime, minDistance):
        gps.start(minTime, minDistance)

    @mainthread
    def on_location(self, **kwargs):
        self.gps_location = f"lat: {kwargs['lat']}  lon: {kwargs['lon']}"
        self.last_call_coord['lat'] = kwargs['lat']
        self.last_call_coord['lon'] = kwargs['lon']
        print(kwargs['lat'], kwargs['lon'], file=open('coords.txt', 'w'))

    @mainthread
    def on_status(self, stype, status):
        self.gps_status = 'type={}\n{}'.format(stype, status)

    def on_start(self):
        self.waiting_for_gps()
        if platform == "android":
            self.start_service()

    def build(self):
        if platform == "android":
            try:
                gps.configure(on_location=self.on_location,
                              on_status=self.on_status)
            except NotImplementedError:
                import traceback
                traceback.print_exc()
                self.gps_status = 'GPS is not implemented for your platform'
            print("gps.py: Android detected. Requesting permissions")
            self.request_android_permissions()

        return Builder.load_string(kv)


if __name__ == "__main__":
    LabelBase.register(name="Poppins", fn_regular="fonts/Poppins-Medium.ttf")
    LabelBase.register(name="BPoppins", fn_regular="fonts/Poppins-SemiBold.ttf")
    WeatherApp().run()
