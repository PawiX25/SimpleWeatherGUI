import requests
import argparse

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

        print(f"\nWeather in {city_name}, {region}, {country}:")
        print(f"Condition: {condition}")
        print(f"Temperature: {temperature}")
        print(f"Humidity: {humidity}%")
        print(f"Wind: {wind_speed}")
    except requests.RequestException as e:
        print(f"Error fetching weather data: {e}")
    except KeyError as e:
        print(f"Unexpected data structure: {e}")

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
        print(f"\nForecast for {city}:")
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

            print(f"{date}: {condition} - High: {max_temp}, Low: {min_temp}")
    except requests.RequestException as e:
        print(f"Error fetching forecast data: {e}")
    except KeyError as e:
        print(f"Unexpected data structure: {e}")

def main():
    parser = argparse.ArgumentParser(description="Get weather and forecast data.")
    parser.add_argument('city', type=str, help="City name to get the weather and forecast for.")
    parser.add_argument('--days', type=int, default=3, help="Number of forecast days (1-10). Default is 3.")
    parser.add_argument('--unit', type=str, choices=['C', 'F'], default='C', help="Unit for temperature (C or F). Default is C.")

    args = parser.parse_args()
    city = args.city
    days = args.days
    unit = args.unit

    if days < 1 or days > 10:
        print("Error: Number of days must be between 1 and 10.")
        return

    get_weather(city, unit)
    get_forecast(city, days, unit)

if __name__ == '__main__':
    main()
