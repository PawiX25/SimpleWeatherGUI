import requests
import sys

API_KEY = 'api_key'
BASE_URL = 'http://api.weatherapi.com/v1/current.json'

def get_weather(city):
    params = {
        'key': API_KEY,
        'q': city,
        'aqi': 'no'
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
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
        print(f"Weather in {city_name}, {region}, {country}:")
        print(f"Condition: {condition}")
        print(f"Temperature: {temperature_c}°C ({temperature_f}°F)")
        print(f"Humidity: {humidity}%")
        print(f"Wind: {wind_kph} kph ({wind_mph} mph)")
    else:
        print(f"Error: Unable to get weather data for {city}. Please check the city name.")

def main():
    if len(sys.argv) != 2:
        print("Usage: python weather.py <city_name>")
        sys.exit(1)
    city = sys.argv[1]
    get_weather(city)

if __name__ == '__main__':
    main()
