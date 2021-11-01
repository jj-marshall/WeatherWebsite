import requests
import datetime
from .models import Location_Data

from django.core.files import File

# The basic api and api key for the Met office data.
base_api = 'http://datapoint.metoffice.gov.uk/public/data/'
api_key = 'PLACEHOLDER'

location_list_api = base_api + 'val/wxfcs/all/json/sitelist?' + api_key
map_layer_list_api = base_api + 'layer/wxfcs/all/json/capabilities?' + api_key

def return_location_data():
    # Returns a list of the individual dictionaries, containing the name and ID for the different locations.
    
    data = requests.get(location_list_api).json()

    formated_data = []
    names = []

    for item in data['Locations']['Location']:
        
        d = {'name':item['name'],
            'id':item['id'],
            }
        
        if item['name'] not in names:
            formated_data.append(d)
        else:
            pass

        names.append(item['name'])

    formated_data.sort(key=lambda item: item.get('name'))
    
    return formated_data


def build_location_database():
    # Builds a database of all locations and the url needed to acsess their specific weather data.
    Location_Data.objects.all().delete()

    data = return_location_data()

    for item in data:
        item = Location_Data(name=item['name'], url=base_api + 'val/wxfcs/all/json/' + item['id'] + '?' + 'res=3hourly&' + api_key)
        item.save()


def return_weather_data(location_name):
    # Returns the next 5 days (3 hourly) of weather data for the selected location.
    item = Location_Data.objects.get(name=location_name)
    item = item.url

    data = requests.get(item).json()
    last_updated = data['SiteRep']['DV']['dataDate']
    data = data['SiteRep']['DV']['Location']['Period']

    formated_data = []

    for item in data:
        data = item['Rep']

        new_day = []

        for item in data:
            if item['$'] == '0':

                new_entry = {'time':'00:00', 'F':item['F'], 'H':item['H'], 'T':item['T'], 'D':item['D'], 'S':item['S'], 'Pp':item['Pp']}

                new_day.append(new_entry)
            
            elif item['$'] == '180':

                new_entry = {'time':'03:00', 'F':item['F'], 'H':item['H'], 'T':item['T'], 'D':item['D'], 'S':item['S'], 'Pp':item['Pp']}

                new_day.append(new_entry)
            
            elif item['$'] == '360':

                new_entry = {'time':'06:00', 'F':item['F'], 'H':item['H'], 'T':item['T'], 'D':item['D'], 'S':item['S'], 'Pp':item['Pp']}

                new_day.append(new_entry)
            
            elif item['$'] == '540':

                new_entry = {'time':'09:00', 'F':item['F'], 'H':item['H'], 'T':item['T'], 'D':item['D'], 'S':item['S'], 'Pp':item['Pp']}

                new_day.append(new_entry)
            
            elif item['$'] == '720':

                new_entry = {'time':'12:00', 'F':item['F'], 'H':item['H'], 'T':item['T'], 'D':item['D'], 'S':item['S'], 'Pp':item['Pp']}

                new_day.append(new_entry)
            
            elif item['$'] == '900':

                new_entry = {'time':'15:00', 'F':item['F'], 'H':item['H'], 'T':item['T'], 'D':item['D'], 'S':item['S'], 'Pp':item['Pp']}

                new_day.append(new_entry)
            
            elif item['$'] == '1080':

                new_entry = {'time':'18:00', 'F':item['F'], 'H':item['H'], 'T':item['T'], 'D':item['D'], 'S':item['S'], 'Pp':item['Pp']}

                new_day.append(new_entry)
            
            elif item['$'] == '1260':

                new_entry = {'time':'21:00', 'F':item['F'], 'H':item['H'], 'T':item['T'], 'D':item['D'], 'S':item['S'], 'Pp':item['Pp']}

                new_day.append(new_entry)

        formated_data.append(new_day)

    formated_data.append(last_updated)

    return formated_data


def format_todays_weather_data(weather_data):
    # Formats the todays weather data of a selected location to fit with the timestamps in the html file, data has to have come from the return weather data function.
    data = weather_data
    data = data[0]

    dna = {
        'F': '-', 
        'H': '-', 
        'T': '-', 
        'D': '-', 
        'S': '-', 
        'Pp': '-'    
    }

    formated_data = {
        '0000':dna,
        '0300':dna,
        '0600':dna,
        '0900':dna,
        '1200':dna,
        '1500':dna,
        '1800':dna,
        '2100':dna
    }
        
    for item in data:
        if item['time'] == '00:00':
            formated_data['0000'] = item

        elif item['time'] == '03:00':
            formated_data['0300'] = item

        elif item['time'] == '06:00':
            formated_data['0600'] = item

        elif item['time'] == '09:00':
            formated_data['0900'] = item

        elif item['time'] == '12:00':
            formated_data['1200'] = item

        elif item['time'] == '15:00':
            formated_data['1500'] = item

        elif item['time'] == '18:00':
            formated_data['1800'] = item

        elif item['time'] == '21:00':
            formated_data['2100'] = item

    return formated_data


def return_weather_type(location_name):
    item = Location_Data.objects.get(name=location_name)
    item = item.url

    data = requests.get(item).json()
    data = data['SiteRep']['DV']['Location']['Period']

    primary = []
    secondary = []

    for item in data:
        data = item['Rep']

        for item in data:
            if item['$'] == '720':
                new_day = format_weather_type(item)
                primary.append(new_day)

            elif item['$'] == '1080':
                new_day = format_weather_type(item)
                secondary.append(new_day)

            else:
                pass

    if len(primary) == 5:
        formated_data = primary
    else:
        formated_data = secondary

    return formated_data


def format_weather_type(weather_type_data):
    item = weather_type_data

    new_day = []

    if item['W'] == '0':
        new_entry = 'Clear throughout the night'
        new_day.append(new_entry)
    
    elif item['W'] == '1':
        new_entry = 'Sunny throughout the day'
        new_day.append(new_entry)
    
    elif item['W'] == '2':
        new_entry = 'Partly cloudy'
        new_day.append(new_entry)

    elif item['W'] == '3':
        new_entry = 'Partly cloudy'
        new_day.append(new_entry)

    elif item['W'] == '5':
        new_entry = 'Mist'
        new_day.append(new_entry)

    elif item['W'] == '6':
        new_entry = 'Fog'
        new_day.append(new_entry)

    elif item['W'] == '7':
        new_entry = 'Cloudy intervals throughout the day'
        new_day.append(new_entry)

    elif item['W'] == '8':
        new_entry = 'Overcast throughout the day'
        new_day.append(new_entry)

    elif item['W'] == '9':
        new_entry = 'Light rain showers'
        new_day.append(new_entry)

    elif item['W'] == '10':
        new_entry = 'Light rain showers'
        new_day.append(new_entry)

    elif item['W'] == '11':
        new_entry = 'Drizzle throughout the day'
        new_day.append(new_entry)

    elif item['W'] == '12':
        new_entry = 'Light rain throughout the day'
        new_day.append(new_entry)

    elif item['W'] == '13':
        new_entry = 'Heavy rain showers'
        new_day.append(new_entry)

    elif item['W'] == '14':
        new_entry = 'Heavy rain showers'
        new_day.append(new_entry)

    elif item['W'] == '15':
        new_entry = 'Heavy rain throughout the day'
        new_day.append(new_entry)

    elif item['W'] == '16':
        new_entry = 'Sleet showers'
        new_day.append(new_entry)

    elif item['W'] == '17':
        new_entry = 'Sleet showers'
        new_day.append(new_entry)

    elif item['W'] == '18':
        new_entry = 'Sleet throughout the day'
        new_day.append(new_entry)

    elif item['W'] == '19':
        new_entry = 'Hail showers'
        new_day.append(new_entry)

    elif item['W'] == '20':
        new_entry = 'Hail showers'
        new_day.append(new_entry)

    elif item['W'] == '21':
        new_entry = 'Hail throughout the day'
        new_day.append(new_entry)

    elif item['W'] == '22':
        new_entry = 'Light snow showers'
        new_day.append(new_entry)

    elif item['W'] == '23':
        new_entry = 'Light snow showers'
        new_day.append(new_entry)

    elif item['W'] == '24':
        new_entry = 'Light snow throughout the day'
        new_day.append(new_entry)

    elif item['W'] == '25':
        new_entry = 'Heavy snow showers'
        new_day.append(new_entry)

    elif item['W'] == '26':
        new_entry = 'Heavy snow showers'
        new_day.append(new_entry)

    elif item['W'] == '27':
        new_entry = 'Heavy snow throughout the day'
        new_day.append(new_entry)

    elif item['W'] == '28':
        new_entry = 'Thunder showers'
        new_day.append(new_entry)

    elif item['W'] == '29':
        new_entry = 'Thunder showers'
        new_day.append(new_entry)

    elif item['W'] == '30':
        new_entry = 'Thunderstorms throughout the day'
        new_day.append(new_entry)

    return new_day


def return_last_updated(weather_data):
    # Returns the date and the time that the weather data was last updated.
    data = weather_data[5]
    
    data = data.replace('-', '/')
    data = data.replace('T', ' at ')
    formated_data = data.replace(':00Z', '')
    
    return formated_data


def return_layer_data():
    # Returns a list of the URLs needed to acsess the different images (3 hourly) of the radar data (rain forecast). 
    data = requests.get(map_layer_list_api).json()
    data = data['Layers']['Layer'][0]['Service']

    layer_name = data['LayerName']
    default_time = data['Timesteps']['@defaultTime']

    formated_data = []

    ts = 0

    while ts != 39:
        ts = str(ts)
        uri = base_api + 'layer//wxfcs//Precipitation_Rate//png?RUN=' + default_time + 'Z&FORECAST=' + ts + '&' + api_key
        formated_data.append(uri)
        ts = int(ts)

        ts += 3

    return formated_data


def build_layer_database():
    # Creates / replaces a series of files with rainfall overlay images.
    data = return_layer_data()
    n = 1
    
    for item in data:
        filename = f'rainfall_image{n}.png'
        n+=1

        r = requests.get(item) 
        with open(f'/Users/joemarshall/OneDrive/CodingProjects/WeatherWebApp/weather_app_main/media/rainfall_overlays/{filename}', 'wb') as f:
            f.write(r.content)


def return_next_5_days():
    # Returns the next 5 days.
    data = []
    formated_data = []
    
    base = datetime.datetime.today()
    
    for x in range(0, 5):
        data.append(base + datetime.timedelta(days=x))
    
    for item in data:
        new_day = item.weekday()

        if new_day == 0:
            formated_data.append('Monday')
        elif new_day == 1:
            formated_data.append('Tuesday')
        elif new_day == 2:
            formated_data.append('Wednesday')
        elif new_day == 3:
            formated_data.append('Thursday')
        elif new_day == 4:
            formated_data.append('Friday')
        elif new_day == 5:
            formated_data.append('Saturday')
        elif new_day == 6:
            formated_data.append('Sunday')

    return(formated_data)

