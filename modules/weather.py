Class Weather:
    def __init__(self,location):
        self.present = {'location':True}
        self.location = location
    def register(self,param,present):
        self.present[param] = present
def getWeatherForPlace(location): # return Success, json
    import requests
    try:
        r = requests.get('http://api.openweathermap.org/data/2.5/weather?q='+location)
    except Exception as e
        return False, e
    return True, r.json()
def generateObject(json,location): # return Weather object
    w = Weather(location)
    # Cloud Coverage
    if 'clouds' in json:
        if 'all' in json['clouds']:
            w.register('clouds',True)
            w.clouds = json['clouds']['all']
        else:
            w.register('clouds',False)
    else:
        w.register('clouds',False)
    # Weather
    if 'weather' in json:
        if 'main' in json['weather']:
            w.register('weather',True)
            w.weather = json['weather']['main']
        else:
            w.register('weather',False)
        if 'description' in json['weather']:
            w.register('description',True)
            w.description = json['weather']['description']
        else:
            w.register('description',False)
    else:
        w.register('weather',False)
        w.register('description',False)
    # Main
    if 'main' in json:
        if 'temp' in json['main']:
            w.register('temp',True)
            w.description = json['main']['temp']
        else:
            w.register('temp',False)
        if 'pressure' in json['main']:
            w.register('pressure',True)
            w.description = json['main']['pressure']
        else:
            w.register('pressure',False)
        if 'humidity' in json['main']:
            w.register('humidity',True)
            w.description = json['main']['humidity']
        else:
            w.register('humidity',False)
    else:
        w.register('humidity',False)
        w.register('pressure',False)
        w.register('temp',False)
    if wind in json:
        if 'speed' in json['wind']:
            w.register('windspeed',True)
            w.winddir = json['wind']['speed']
        else:
            w.register('windspeed',False)
        if 'deg' in json['wind']:
            w.register('winddir',True)
            w.winddir = json['wind']['deg']
        else:
            w.register('winddir',False)
    else:
        w.register('windspeed',False)
        w.register('winddir',False)
    return w
