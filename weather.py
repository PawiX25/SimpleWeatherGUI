import requests
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
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
            messagebox.showerror("Error", data['error']['message'])
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
            temperature = f"{temperature_f:.1f}°F"
            feels_like = f"{feels_like_f:.1f}°F"
            wind_speed = f"{wind_mph:.1f} mph"
            precipitation = f"{precip_in:.1f} in"
        else:
            temperature = f"{temperature_c:.1f}°C"
            feels_like = f"{feels_like_c:.1f}°C"
            wind_speed = f"{wind_kph:.1f} kph"
            precipitation = f"{precip_mm:.1f} mm"

        weather_data = {
            "City": city_name,
            "Region": region,
            "Country": country,
            "Condition": condition,
            "Temperature": temperature,
            "Feels Like": feels_like,
            "Humidity": f"{humidity}%",
            "Wind Speed": wind_speed,
            "Wind Direction": wind_dir,
            "UV Index": uv_index,
            "Precipitation": precipitation
        }

        return weather_data

    except requests.RequestException as e:
        messagebox.showerror("Error", f"Error fetching weather data for {city}: {e}")
        return None

def get_forecast(city, days, unit):
    if days < 1 or days > 10:
        messagebox.showerror("Error", "Forecast days must be between 1 and 10.")
        return None, [], [], [], [], []

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
            messagebox.showerror("Error", data['error']['message'])
            return None, [], [], [], [], []

        forecast = data['forecast']['forecastday']

        forecast_data = []
        dates = []
        high_temps = []
        low_temps = []
        precipitations = []
        uv_indexes = []

        for day in forecast:
            date = day['date']
            condition = day['day']['condition']['text']
            max_temp_c = day['day']['maxtemp_c']
            min_temp_c = day['day']['mintemp_c']
            max_temp_f = day['day']['maxtemp_f']
            min_temp_f = day['day']['mintemp_f']
            precip_mm = day['day']['totalprecip_mm']
            precip_in = day['day']['totalprecip_in']
            uv_index = day['day']['uv']

            if unit.upper() == 'F':
                max_temp = f"{max_temp_f:.1f}°F"
                min_temp = f"{min_temp_f:.1f}°F"
                precipitation = f"{precip_in:.1f} in"
                high_temps.append(max_temp_f)
                low_temps.append(min_temp_f)
            else:
                max_temp = f"{max_temp_c:.1f}°C"
                min_temp = f"{min_temp_c:.1f}°C"
                precipitation = f"{precip_mm:.1f} mm"
                high_temps.append(max_temp_c)
                low_temps.append(min_temp_c)

            forecast_data.append({
                "Date": date,
                "Condition": condition,
                "High Temp": max_temp,
                "Low Temp": min_temp,
                "Chance of Rain": f"{day['day']['daily_chance_of_rain']}%",
                "Precipitation": precipitation
            })
            dates.append(date)
            precipitations.append(precip_mm if unit.upper() == 'C' else precip_in)
            uv_indexes.append(uv_index)

        return forecast_data, dates, high_temps, low_temps, precipitations, uv_indexes

    except requests.RequestException as e:
        messagebox.showerror("Error", f"Error fetching forecast data for {city}: {e}")
        return None, [], [], [], [], []

def plot_forecast(dates, high_temps, low_temps, precipitations, uv_indexes):
    if not dates or not high_temps or not low_temps:
        raise ValueError("No data available for plotting.")

    fig, ax1 = plt.subplots(figsize=(12, 6))

    ax1.plot(dates, high_temps, label='High Temp', marker='o', color='red', linestyle='-', linewidth=2)
    ax1.plot(dates, low_temps, label='Low Temp', marker='o', color='blue', linestyle='-', linewidth=2)
    ax1.set_xlabel('Date', fontsize=12)
    ax1.set_ylabel('Temperature (°C or °F)', fontsize=12)
    ax1.set_title('Weather Trends', fontsize=14)
    ax1.legend(loc='upper left')
    ax1.grid(True)
    plt.xticks(rotation=45, ha='right', fontsize=10)

    ax2 = ax1.twinx()
    ax2.plot(dates, precipitations, label='Precipitation', marker='s', color='green', linestyle='--', linewidth=2)
    ax2.plot(dates, uv_indexes, label='UV Index', marker='^', color='purple', linestyle='--', linewidth=2)
    ax2.set_ylabel('Precipitation (mm or in) / UV Index', fontsize=12)
    ax2.legend(loc='upper right')

    plt.tight_layout()
    return fig

def display_weather_and_forecast():
    city = city_entry.get()
    days = int(days_entry.get())
    unit = unit_combobox.get()

    weather_data = get_weather(city, unit)
    if weather_data:
        forecast_data, dates, high_temps, low_temps, precipitations, uv_indexes = get_forecast(city, days, unit)
        if forecast_data:

            weather_tree.delete(*weather_tree.get_children())
            for key, value in weather_data.items():
                weather_tree.insert('', 'end', values=(key, value))

            forecast_tree.delete(*forecast_tree.get_children())
            for item in forecast_data:
                forecast_tree.insert('', 'end', values=(item["Date"], item["Condition"], item["High Temp"], item["Low Temp"], item["Chance of Rain"], item["Precipitation"]))

            try:
                fig = plot_forecast(dates, high_temps, low_temps, precipitations, uv_indexes)
                for widget in plot_frame.winfo_children():
                    widget.destroy()
                canvas = FigureCanvasTkAgg(fig, master=plot_frame)
                canvas.draw()
                canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            except ValueError as ve:
                messagebox.showerror("Error", str(ve))
        else:
            messagebox.showerror("Error", "Unexpected format for forecast data.")

def save_to_file():
    city = city_entry.get()
    days = int(days_entry.get())
    unit = unit_combobox.get()

    weather_data = get_weather(city, unit)
    if weather_data:
        forecast_data, _, _, _, _, _ = get_forecast(city, days, unit)
        if forecast_data:
            output_file = 'weather_forecast.csv'
            with open(output_file, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Weather for", city])
                writer.writerow(["City", "Region", "Country", "Condition", "Temperature", "Feels Like", "Humidity", "Wind Speed", "Wind Direction", "UV Index", "Precipitation"])
                for key, value in weather_data.items():
                    writer.writerow([f"{key}: {value}"])
                writer.writerow([])
                writer.writerow(["Forecast for", city])
                writer.writerow(["Date", "Condition", "High Temp", "Low Temp", "Chance of Rain", "Precipitation"])
                for item in forecast_data:
                    writer.writerow([f"{key}: {value}" for key, value in item.items()])
                writer.writerow([])
            messagebox.showinfo("Success", f"Data saved to {output_file}.")
        else:
            messagebox.showerror("Error", "Unexpected format for forecast data.")

root = tk.Tk()
root.title("Weather Application")

tk.Label(root, text="City:").grid(row=0, column=0, padx=5, pady=5)
city_entry = tk.Entry(root)
city_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Number of Days:").grid(row=1, column=0, padx=5, pady=5)
days_entry = tk.Entry(root)
days_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Unit:").grid(row=2, column=0, padx=5, pady=5)
unit_combobox = ttk.Combobox(root, values=["C", "F"])
unit_combobox.grid(row=2, column=1, padx=5, pady=5)
unit_combobox.set("C")

tk.Button(root, text="Get Weather and Forecast", command=display_weather_and_forecast).grid(row=3, column=0, columnspan=2, padx=5, pady=5)
tk.Button(root, text="Save to File", command=save_to_file).grid(row=4, column=0, columnspan=2, padx=5, pady=5)

weather_tree = ttk.Treeview(root, columns=("Attribute", "Value"), show='headings')
weather_tree.heading("Attribute", text="Attribute")
weather_tree.heading("Value", text="Value")
weather_tree.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

forecast_tree = ttk.Treeview(root, columns=("Date", "Condition", "High Temp", "Low Temp", "Chance of Rain", "Precipitation"), show='headings')
forecast_tree.heading("Date", text="Date")
forecast_tree.heading("Condition", text="Condition")
forecast_tree.heading("High Temp", text="High Temp")
forecast_tree.heading("Low Temp", text="Low Temp")
forecast_tree.heading("Chance of Rain", text="Chance of Rain")
forecast_tree.heading("Precipitation", text="Precipitation")
forecast_tree.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

plot_frame = tk.Frame(root)
plot_frame.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()
