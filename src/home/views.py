from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views import View
import environ
import datetime
import requests
import json
import pathlib

env = environ.Env()


def load_demo_data():
    with open(settings.DEMO_DATA_PATH, "r") as file:
        return json.load(file)


def homepage_view(request):

    # Get weather data to render them home page
    # context = display_weather(request, context)

    return render(request, "home/index.html")


def display_weather(request, context):
    api_key = env.str("WEATHER_API_KEY")
    weather_url = "https://api.openweathermap.org/data/3.0/onecall?lat={}&lon={}&exclude=hourly,minutely,alerts&units=metric&appid={}&lang=fr"

    if request.method == "POST":
        city = request.POST['city']

        # Verify if form is submitted empty
        if not city:
            context['error_message'] = "Veuillez saisir une ville."
            return context

        # Verify if city is not found
        lat, lon = get_coordinates(city, api_key)
        if lat is None and lon is None:
            context['error_message'] = "La ville que vous avez choisie n'existe pas"
            return context

        current_weather, daily_weather = fetch_weather_data(
            city, api_key, weather_url)
        context.update({
            "current_weather": current_weather,
            "daily_weather": daily_weather
        })

    return context


def get_coordinates(city, api_key):
    convert_city_to_coord = "https://api.openweathermap.org/geo/1.0/direct?q={}&appid={}"
    response = requests.get(convert_city_to_coord.format(city, api_key)).json()

    # Check if response is empty
    if not response:
        return None, None

    lat = response[0]['lat']
    lon = response[0]['lon']

    return lat, lon


def fetch_weather_data(city, api_key, weather_url):
    lat, lon = get_coordinates(city, api_key)
    response_weather_data = requests.get(
        weather_url.format(lat, lon, api_key)).json()

    current_weather = {
        "city": city,
        "coordinate": f"lat {str(round(response_weather_data['lat'], 2))}° lon {str(round(response_weather_data['lon'], 2))}°",
        "description": str(response_weather_data['current']['weather'][0]['description']),
        "icon": str(response_weather_data['current']['weather'][0]['icon']),
        "temperature": str(round(response_weather_data['current']['temp'], 1)) + " °C",
        "humidity": str(response_weather_data['current']['humidity']),
        "wind": str(round(response_weather_data['current']['wind_speed'] * 3.6, 1)),
        "clouds": str(response_weather_data['current']['clouds']),
    }

    daily_weather = []
    forecast_dates = []
    for daily_data in response_weather_data['daily'][:]:
        daily_weather.append({
            "date": datetime.datetime.fromtimestamp(daily_data['dt']).date(),
            "sunrise": datetime.datetime.fromtimestamp(daily_data['sunrise']).strftime('%H:%M:%S'),
            "sunset": datetime.datetime.fromtimestamp(daily_data['sunset']).strftime('%H:%M:%S'),
            "moonrise": datetime.datetime.fromtimestamp(daily_data['moonrise']).strftime('%H:%M:%S'),
            "moonset": datetime.datetime.fromtimestamp(daily_data['moonset']).strftime('%H:%M:%S'),
            "min_temp": str(round(daily_data['temp']['min'], 1)) + " °C",
            "max_temp": str(round(daily_data['temp']['max'], 1)) + " °C",
            "description": str(daily_data['weather'][0]['description']),
            "icon": str(daily_data['weather'][0]['icon']),
            "clouds": str(daily_data['clouds']),
            "wind": str(round(daily_data['wind_speed'] * 3.6, 1)),
            "rain": str(round(daily_data['pop'] * 100)) + "%"
        })

    return current_weather, daily_weather


def proxy_to_aladin(request):
    target_url = request.GET.get(
        'url', 'https://aladin.u-strasbg.fr/AladinLite/api')

    response = requests.get(target_url)

    http_response = HttpResponse(
        response.content, content_type=response.headers['Content-Type'])

    http_response['Access-Control-Allow-Origin'] = '*'
    http_response['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
    http_response['Access-Control-Allow-Headers'] = 'Content-Type'
    return http_response


class FetchEquipment(View):
    def get(self, request, *args, **kwargs):
        demo_data = load_demo_data()
        telescopes = demo_data.get("telescopes", [])
        cameras = demo_data.get("cameras", [])

        return JsonResponse({'telescopes': telescopes, 'cameras': cameras})
