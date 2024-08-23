# Weather Forecast Application

This Python application provides a graphical user interface (GUI) to retrieve current weather and forecast data using the WeatherAPI. It supports fetching weather information for any city and allows you to view and save both current conditions and forecasts. Additionally, it visualizes temperature trends and other weather data.

## Features

- **Current Weather**: Get the latest weather information for any city.
- **Forecast**: Retrieve weather forecasts for up to 10 days.
- **Units**: Choose between Celsius and Fahrenheit for temperature units.
- **Data Visualization**: Plot temperature trends and other weather data using Matplotlib.
- **Data Saving**: Save weather and forecast data to a CSV file.
- **Theme Management**: Change the application theme using `ttkthemes`.
- **Settings**: Configure API key, default unit, and default city via a settings window.

## Requirements

- Python 3.x
- `requests` library
- `matplotlib` library
- `csv` library (standard with Python)
- `ttkthemes` library
- `tkinter` library (standard with Python)

You can install the required libraries using pip:

```bash
pip install requests matplotlib ttkthemes
```

## Setup

1. **API Key**: Obtain an API key from [WeatherAPI](https://www.weatherapi.com/) and replace `'api_key'` in the script with your actual API key.

2. **Save the Script**: Save the script to a file, for example, `weather_application.py`.

3. **Run the Application**: Execute the script to open the GUI.

## Usage

1. **City Entry**: Enter the city name in the provided text entry field.

2. **Number of Days**: Specify the number of days for the forecast (1-10).

3. **Unit Selection**: Choose the temperature unit (Celsius or Fahrenheit) from the dropdown menu.

4. **Plot Style**: Select the desired plot style (Line, Bar, Scatter, Area) for visualizing temperature trends.

5. **Fetch Weather and Forecast**: Click the "Get Weather and Forecast" button to retrieve and display data.

6. **Save Data**: Click the "Save to File" button to save the weather and forecast data to a CSV file.

7. **Settings**: Configure your API key, default unit, and default city via the "Settings" menu.

8. **Change Theme**: Select different themes from the "Themes" menu to customize the appearance of the application.

## Examples

1. **Fetch Weather and Forecast**:
   - Enter the city, number of days, unit, and plot style in the GUI, then click "Get Weather and Forecast".

2. **Save Data**:
   - Click "Save to File" to save the data as a CSV file with the name format `{city}_weather_forecast.csv`.

## Output

- **GUI Output**: Displays current weather and forecast in tabular format and a plot of temperature trends.
- **CSV Output**: If saving is selected, the data will be written to a CSV file with details of current weather and forecast.

## Error Handling

- **API Errors**: Appropriate error messages will be shown if there are issues with API requests.
- **Invalid Inputs**: Errors will be displayed if the input values are invalid (e.g., non-integer days, unsupported units).

## Acknowledgments

- [WeatherAPI](https://www.weatherapi.com/) for providing the weather data.
- [Matplotlib](https://matplotlib.org/) for plotting the temperature trends.
- [ttkthemes](https://pypi.org/project/ttkthemes/) for providing theme support in Tkinter.
