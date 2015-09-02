import datetime
import common
from common import requests
class Weather:
    def __init__(self,location):
        self.present = {'location':True}
        self.location = location
    def register(self,param,present):
        self.present[param] = present
def getWeatherForPlace(location): # return success(Bool), json(JSON string)/exception(Exception)
    try:
        r = requests.get('http://api.openweathermap.org/data/2.5/weather?q='+location)
    except Exception as e:
        print e
        return False, e
    return True, r.json()
def generateObject(jsonString,location): # return weather(Weather)
    j = json.loads(jsonString)
    w = Weather(location)
    # Cloud Coverage
    if 'clouds' in j:
        if 'all' in j['clouds']:
            w.register('clouds',True)
            w.clouds = j['clouds']['all']
        else:
            w.register('clouds',False)
    else:
        w.register('clouds',False)
    # Weather
    if 'weather' in j:
        if 'main' in j['weather'][0]:
            w.register('weather',True)
            w.weather = j['weather'][0]['main']
        else:
            w.register('weather',False)
        if 'description' in j['weather'][0]:
            w.register('description',True)
            w.description = j['weather'][0]['description']
        else:
            w.register('description',False)
    else:
        w.register('weather',False)
        w.register('description',False)
    # Main
    if 'main' in j:
        if 'temp' in j['main']:
            w.register('temp',True)
            w.temp = j['main']['temp']
        else:
            w.register('temp',False)
        if 'pressure' in j['main']:
            w.register('pressure',True)
            w.pressure = j['main']['pressure']
        else:
            w.register('pressure',False)
        if 'humidity' in j['main']:
            w.register('humidity',True)
            w.humidity = j['main']['humidity']
        else:
            w.register('humidity',False)
        if 'temp_min' in j['main']:
            w.register('temp_min',True)
            w.temp_min = j['main']['temp_min']
        else:
            w.register('temp_min',False)
        if 'temp_max' in j['main']:
            w.register('temp_max',True)
            w.temp_max = j['main']['temp_max']
        else:
            w.register('temp_max',False)
    else:
        w.register('humidity',False)
        w.register('pressure',False)
        w.register('temp',False)
    if 'wind' in j:
        if 'speed' in j['wind']:
            w.register('windspeed',True)
            w.windspeed = j['wind']['speed']
        else:
            w.register('windspeed',False)
        if 'deg' in j['wind']:
            w.register('winddir',True)
            w.winddir = j['wind']['deg']
        else:
            w.register('winddir',False)
    else:
        w.register('windspeed',False)
        w.register('winddir',False)
    if 'sys' in j:
        if 'sunrise' in j['sys']:
            w.register('sunrise',True)
            w.sunrise = j['sys']['sunrise']
        else:
            w.register('sunrise',False)
        if 'sunset' in j['sys']:
            w.register('sunset',True)
            w.sunset = j['sys']['sunset']
        else:
            w.register('sunset',False)
    else:
        w.register('sunrise',False)
        w.register('sunset',False)
    return w
def getDirFromBearing(bearing): # return compassDirection(String)
    bearing = bearing%360
    if bearing < 12:
        return "N"
    elif bearing < 34:
        return "NNE"
    elif bearing < 57:
        return "NE"
    elif bearing < 79:
        return "ENE"
    elif bearing < 102:
        return "E"
    elif bearing < 124:
        return "ESE"
    elif bearing < 147:
        return "SE"
    elif bearing < 169:
        return "SSE"
    elif bearing < 192:
        return "S"
    elif bearing < 214:
        return "SSE"
    elif bearing < 237:
        return "S"
    elif bearing < 259:
        return "ENE"
    elif bearing < 282:
        return "E"
    elif bearing < 304:
        return "NNE"
    elif bearing < 327:
        return "NE"
    elif bearing < 349:
        return "ENE"
    else:
        return "N"
def constructString(w): # weather description temp pressure humidity clouds windspeed winddir sunrise sunset
    return ("The weather"+((" in "+w.location) if w.present['location'] else "")+" is"+((" "+w.weather+(" ("+w.description+")"if w.present['description'] else "")) if w.present['weather'] else " unspecified")+((" at a temperature of "+str(int(w.temp)-273)+"C"+(" (min "+str(int(w.temp_min)-273)+"C max "+str(int(w.temp_max)-273)+"C)" if w.present['temp_min'] and w.present['temp_max'] else "")) if w.present['temp'] else "")+((" with a pressure of "+str(w.pressure)+"hPa ("+"{0:.3f}".format(float(w.pressure)/1000.0)+" bar)") if w.present['pressure'] else "")+((" and a humidity of "+str(w.humidity)+"%") if w.present['humidity'] else "")+((" and a cloud coverage of "+str(w.clouds)+"%") if w.present['clouds'] else "")+((" and wind speed "+str(w.windspeed)+"m/s from bearing {0:03d} ({1})".format(int(w.winddir),getDirFromBearing(int(w.winddir)))) if w.present['winddir'] and w.present['windspeed'] else "")+("\nSunrise: {0}, Sunset: {1}".format(datetime.datetime.fromtimestamp(int(w.sunrise)).strftime('%H:%M:%S'),datetime.datetime.fromtimestamp(int(w.sunset)).strftime('%H:%M:%S')) if w.present['sunrise'] and w.present['sunset'] else ""))
def stringFromLocation(location):
    success, weather = getWeatherForPlace(location)
    if success:
        return (constructString(generateObject(str(weather).replace("u'","'").replace("'",'"'),location)))
    else:
        return "Exception: "+str(weather)
def getSavedData(nick):
    data = common.persistence.confLoad("weatherLocations",{})
    if nick in data:
        return data[nick]
    else:
        return False
def putSavedData(nick,location):
    data = common.persistence.confLoad("weatherLocations",{})
    data.update({nick:location})
    common.persistence.confSave("weatherlocations",data)
def react(t,irc):
    command,message = common.command(common.type(t))
    if command == "weather":
        args = message['args']
        if len(args) = 0:
            location = getSavedData(message['from'])
            if location == False:
                common.say("Sorry, I don't know where you live. Try \"{0}weather <location>\"".format(common.conf.read()['commands']['commandPrefix']))
            else:
                common.say(stringFromLocation(location))
        else:
            location = " ".join(args)
            putSavedData(message['from'],location)
            common.say(stringFromLocation(location))
