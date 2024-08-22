import requests
import argparse
from tabulate import tabulate
import matplotlib.pyplot as plt
import sys
import csv

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

        if 'error' in data:
            print(f"Error: {data['error']['message']}")
            return None

        location = data['location']
        current = data['current']
        city_name = location['name']
        region = location['region']
        country = location['country']
        temperature_c = current['temp_c']
        temperature_f = current['temp_f']
        feels_like_c = current['feelslike_c']
        feels_like_f = current['feelslike_f']
        condition = current['condition']['text']
        humidity = current['humidity']
        wind_kph = current['wind_kph']
        wind_mph = current['wind_mph']
        wind_dir = current['wind_dir']
        uv_index = current['uv']
        precip_mm = current['precip_mm']
        precip_in = current['precip_in']

        if unit.upper() == 'F':
            temperature = f"{temperature_f}°F"
            feels_like = f"{feels_like_f}°F"
            wind_speed = f"{wind_mph} mph"
            precipitation = f"{precip_in} in"
        else:
            temperature = f"{temperature_c}°C"
            feels_like = f"{feels_like_c}°C"
            wind_speed = f"{wind_kph} kph"
            precipitation = f"{precip_mm} mm"

        weather_data = [
            ["City", "Region", "Country", "Condition", "Temperature", "Feels Like", "Humidity", "Wind Speed", "Wind Direction", "UV Index", "Precipitation"],
            [city_name, region, country, condition, temperature, feels_like, f"{humidity}%", wind_speed, wind_dir, uv_index, precipitation]
        ]
        
        print(f"\nWeather in {city_name}, {region}, {country}:")
        print(tabulate(weather_data, headers='firstrow', tablefmt='grid'))
        
        return weather_data[1] 

    except requests.RequestException as e:
        print(f"Error fetching weather data for {city}: {e}")
        if response.status_code == 401:
            print("Error 401: Unauthorized. Please check your API key.")
        elif response.status_code == 404:
            print(f"Error 404: City {city} not found. Please check the city name.")
        elif response.status_code == 500:
            print("Error 500: Internal Server Error. Please try again later.")
        return None
    except KeyError as e:
        print(f"Unexpected data structure for {city}: {e}")
        return None

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

        if 'error' in data:
            print(f"Error: {data['error']['message']}")
            return None

        forecast = data['forecast']['forecastday']

        forecast_data = [["Date", "Condition", "High Temp", "Low Temp", "Chance of Rain", "Precipitation"]]
        dates = []
        high_temps = []
        low_temps = []

        for day in forecast:
            date = day['date']
            condition = day['day']['condition']['text']
            max_temp_c = day['day']['maxtemp_c']
            min_temp_c = day['day']['mintemp_c']
            max_temp_f = day['day']['maxtemp_f']
            min_temp_f = day['day']['mintemp_f']
            chance_of_rain = day['day']['daily_chance_of_rain']
            precip_mm = day['day']['totalprecip_mm']
            precip_in = day['day']['totalprecip_in']

            if unit.upper() == 'F':
                max_temp = f"{max_temp_f}°F"
                min_temp = f"{min_temp_f}°F"
                precipitation = f"{precip_in} in"
                high_temps.append(max_temp_f)
                low_temps.append(min_temp_f)
            else:
                max_temp = f"{max_temp_c}°C"
                min_temp = f"{min_temp_c}°C"
                precipitation = f"{precip_mm} mm"
                high_temps.append(max_temp_c)
                low_temps.append(min_temp_c)

            forecast_data.append([date, condition, max_temp, min_temp, f"{chance_of_rain}%", precipitation])

        print(f"\nForecast for {city}:")
        print(tabulate(forecast_data, headers='firstrow', tablefmt='grid'))

        dates = [day['date'] for day in forecast]
        plt.figure(figsize=(10, 5))
        plt.plot(dates, high_temps, label='High Temp', marker='o', color='red')
        plt.plot(dates, low_temps, label='Low Temp', marker='o', color='blue')
        plt.xlabel('Date')
        plt.ylabel(f'Temperature ({unit})')
        plt.title(f'Temperature Trend for {city}')
        plt.legend()
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

        return forecast_data[1:]

    except requests.RequestException as e:
        print(f"Error fetching forecast data for {city}: {e}")
        if response.status_code == 401:
            print("Error 401: Unauthorized. Please check your API key.")
        elif response.status_code == 404:
            print(f"Error 404: City {city} not found. Please check the city name.")
        elif response.status_code == 500:
            print("Error 500: Internal Server Error. Please try again later.")
        return None
    except KeyError as e:
        print(f"Unexpected data structure for {city}: {e}")
        return None

def save_to_file(weather_data, forecast_data, city, output_file):
    with open(output_file, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Weather for", city])
        writer.writerow(["City", "Region", "Country", "Condition", "Temperature", "Feels Like", "Humidity", "Wind Speed", "Wind Direction", "UV Index", "Precipitation"])
        writer.writerow(weather_data)
        writer.writerow([])
        writer.writerow(["Forecast for", city])
        writer.writerow(["Date", "Condition", "High Temp", "Low Temp", "Chance of Rain", "Precipitation"])
        writer.writerows(forecast_data)
        writer.writerow([]) 

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
    parser.add_argument('cities', type=str, nargs='*', help="City names to get the weather and forecast for.")
    parser.add_argument('--days', type=int, default=3, help="Number of forecast days (1-10). Default is 3.")
    parser.add_argument('--unit', type=str, choices=['C', 'F'], default='C', help="Unit for temperature (C or F). Default is C.")
    parser.add_argument('--output', type=str, help="Output file to save the weather and forecast data.")

    args = parser.parse_args()

    if not args.cities:
        cities = input("Enter city names (separated by commas): ").split(',')
        cities = [city.strip() for city in cities]
    else:
        cities = args.cities

    if args.days is None:
        days = int(input("Enter number of forecast days (1-10): "))
    else:
        days = args.days

    if args.unit is None:
        unit = input("Enter temperature unit (C or F): ").strip().upper()
        while unit not in ['C', 'F']:
            print("Invalid unit. Please enter 'C' or 'F'.")
            unit = input("Enter temperature unit (C or F): ").strip().upper()
    else:
        unit = args.unit

    for city in cities:
        weather_data = get_weather(city, unit)
        if weather_data:
            forecast_data = get_forecast(city, days, unit)
            if forecast_data and args.output:
                save_to_file(weather_data, forecast_data, city, args.output)

if __name__ == '__main__':
    main()
