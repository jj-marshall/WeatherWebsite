from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Location_Data
from .api_data import return_weather_data, format_todays_weather_data, return_last_updated, return_weather_type, return_next_5_days

def home_page(request):
    # Home page view
    mapbox_key = 'PLACEHOLDER'
    location_data = Location_Data.objects.all()
    selected_location = 'London'
    next_5_days = return_next_5_days()
    weather_type = return_weather_type(selected_location)
    weather_data = return_weather_data(selected_location)
    todays_weather_data = format_todays_weather_data(weather_data)
    last_updated = return_last_updated(weather_data)



    return render(request, 
        'home_page.html',
        {'mapbox_key':mapbox_key,
        'location_data':location_data,
        'selected_location':selected_location,
        'next_5_days':next_5_days,
        'weather_type':weather_type, 
        'weather_data':weather_data,
        'todays_weather_data':todays_weather_data,
        'last_updated':last_updated}
        )


def selected_weather_page(request):
    mapbox_key = 'PLACEHOLDER'
    location_data = Location_Data.objects.all()
    selected_location = request.GET['selected_location'].title().strip(' ')
    next_5_days = return_next_5_days()
    weather_type = return_weather_type(selected_location)
    weather_data = return_weather_data(selected_location)
    todays_weather_data = format_todays_weather_data(weather_data)
    last_updated = return_last_updated(weather_data)

    return render(request,
        'selected_weather_page.html',
        {'mapbox_key':mapbox_key,
        'location_data':location_data,
        'selected_location':selected_location,
        'next_5_days':next_5_days,
        'weather_type':weather_type,
        'weather_data':weather_data,
        'todays_weather_data':todays_weather_data,
        'last_updated':last_updated}
        )
