import requests
import argparse
from tabulate import tabulate

API_KEY = 'api_key'
BASE_URL_CURRENT = 'http://api.weatherapi.com/v1/current.json'
BASE_URL_FORECAST = 'http://api.weatherapi.com/v1/forecast.json'

def get_weather(city, unit):
    params = {
        'key': API_KEY,
        'q': city,
        'aqi': 'no'
    }
    try:
        response = requests.get(BASE_URL_CURRENT, params=params)
        response.raise_for_status()
        data = response.json()
        location = data['location']
        current = data['current']
        city_name = location['name']
        region = location['region']
        country = location['country']
        temperature_c = current['temp_c']
        temperature_f = current['temp_f']
        condition = current['condition']['text']
        humidity = current['humidity']
        wind_kph = current['wind_kph']
        wind_mph = current['wind_mph']

        if unit.upper() == 'F':
            temperature = f"{temperature_f}°F"
            wind_speed = f"{wind_mph} mph"
        else:
            temperature = f"{temperature_c}°C"
            wind_speed = f"{wind_kph} kph"

        weather_data = [
            ["City", "Region", "Country", "Condition", "Temperature", "Humidity", "Wind Speed"],
            [city_name, region, country, condition, temperature, f"{humidity}%", wind_speed]
        ]
        
        print(f"\nWeather in {city_name}, {region}, {country}:")
        print(tabulate(weather_data, headers='firstrow', tablefmt='grid'))
        
    except requests.RequestException as e:
        print(f"Error fetching weather data for {city}: {e}")
    except KeyError as e:
        print(f"Unexpected data structure for {city}: {e}")

def get_forecast(city, days, unit):
    if days < 1 or days > 10:
        print("Error: Forecast days must be between 1 and 10.")
        return

    params = {
        'key': API_KEY,
        'q': city,
        'days': days,
        'aqi': 'no'
    }
    try:
        response = requests.get(BASE_URL_FORECAST, params=params)
        response.raise_for_status()
        data = response.json()
        forecast = data['forecast']['forecastday']

        forecast_data = [["Date", "Condition", "High Temp", "Low Temp"]]
        for day in forecast:
            date = day['date']
            condition = day['day']['condition']['text']
            max_temp_c = day['day']['maxtemp_c']
            min_temp_c = day['day']['mintemp_c']
            max_temp_f = day['day']['maxtemp_f']
            min_temp_f = day['day']['mintemp_f']

            if unit.upper() == 'F':
                max_temp = f"{max_temp_f}°F"
                min_temp = f"{min_temp_f}°F"
            else:
                max_temp = f"{max_temp_c}°C"
                min_temp = f"{min_temp_c}°C"

            forecast_data.append([date, condition, max_temp, min_temp])

        print(f"\nForecast for {city}:")
        print(tabulate(forecast_data, headers='firstrow', tablefmt='grid'))
        
    except requests.RequestException as e:
        print(f"Error fetching forecast data for {city}: {e}")
    except KeyError as e:
        print(f"Unexpected data structure for {city}: {e}")

def main():
    parser = argparse.ArgumentParser(
        description=(
            "Get weather and forecast data.\n\n"
            "Examples:\n"
            "  python script.py London\n"
            "  python script.py London --days 5\n"
            "  python script.py London Paris --unit F\n"
            "  python script.py London --days 7 --unit F\n"
        )
    )
    parser.add_argument('cities', type=str, nargs='+', help="City names to get the weather and forecast for.")
    parser.add_argument('--days', type=int, default=3, help="Number of forecast days (1-10). Default is 3.")
    parser.add_argument('--unit', type=str, choices=['C', 'F'], default='C', help="Unit for temperature (C or F). Default is C.")

    args = parser.parse_args()
    cities = args.cities
    days = args.days
    unit = args.unit

    for city in cities:
        get_weather(city, unit)
        get_forecast(city, days, unit)

if __name__ == '__main__':
    main()
