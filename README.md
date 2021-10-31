# WeatherWebsite

## Description
This website provides weather forecasts for over 5000 locations across the United Kingdom. All data is provided courtesy of the DataPoint service which is offered by the Met Office and is updated every 3 hours. The website is built using the Django web framework and utilises a series of other services including MapBox, to provide a basis for the radar overlays and Bootstrap, to help style the front end.

Please note:
* The Met Office API key has been removed from api_data.py. As such, all weather data is out of date.
* The MapBox API key has been removed from views.py. As such, the interactive map cannot be viewed.

To view the webpage, either add your own keys which can be found on their respective websites or see the Website.pdf file.

* https://www.metoffice.gov.uk/services/data/datapoint
* https://www.mapbox.com/mapbox-gljs

## Running this project locally
1. Clone this project locally.
2. Create a virtual environment. ``` pipenv shell ```
3. Install project dependencies. ``` pipenv install django==3.2.8 django-crontab==0.7.1 requests==2.26.0 ```
4. Run ``` python manage.py runserver ```
5. To view the full webpage add the api keys to their respective files as noted previously.