# Weather Forecast Script

This Python script retrieves current weather and forecast data for specified cities using the WeatherAPI. It supports fetching weather information for multiple cities and can display both current conditions and forecasts. You can also save the data to a CSV file and visualize temperature trends.

## Features

- Get current weather for multiple cities.
- Retrieve weather forecasts for up to 10 days.
- Choose temperature unit (Celsius or Fahrenheit).
- Save weather and forecast data to a CSV file.
- Plot temperature trends using matplotlib.

## Requirements

- Python 3.x
- `requests` library
- `argparse` library (standard with Python)
- `tabulate` library
- `matplotlib` library
- `csv` library (standard with Python)

You can install the required libraries using pip:

    pip install requests tabulate matplotlib

## Setup

1. Obtain an API key from [WeatherAPI](https://www.weatherapi.com/) and replace `'api_key'` in the script with your actual API key.

2. Save the script to a file, for example, `weather_script.py`.

## Usage

### Command Line Arguments

- `cities`: Names of the cities to get weather and forecast data for.
- `--days`: Number of forecast days (1-10). Default is 3.
- `--unit`: Temperature unit (C or F). Default is Celsius.
- `--output`: File path to save the weather and forecast data.

### Examples

1. **Get current weather for London:**

        python weather_script.py London

2. **Get 5-day forecast for London:**

        python weather_script.py London --days 5

3. **Get weather and 7-day forecast for London and Paris with temperature in Fahrenheit:**

        python weather_script.py London Paris --days 7 --unit F

4. **Save weather and forecast data to a CSV file:**

        python weather_script.py London --days 7 --unit F --output weather_data.csv

## Output

- **Console Output**: Displays the current weather and forecast in a tabulated format.
- **CSV Output**: If the `--output` argument is used, the data will be appended to the specified CSV file.
- **Plot**: A temperature trend graph will be displayed if a forecast is retrieved.

## Error Handling

- If there's an issue with the API request, an appropriate error message will be displayed.
- Common errors include unauthorized access (401), city not found (404), and internal server errors (500).

## Acknowledgments

- [WeatherAPI](https://www.weatherapi.com/) for providing the weather data.
- [Matplotlib](https://matplotlib.org/) for plotting the temperature trends.
- [Tabulate](https://pypi.org/project/tabulate/) for formatting the table output.
