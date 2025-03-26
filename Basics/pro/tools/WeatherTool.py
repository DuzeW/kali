import requests
import os
import logging

from crewai.tools import BaseTool
from dotenv import load_dotenv
from urllib.parse import quote


def save_coordinates_to_file(lat, lon, filename="coordinates.txt"):
    try:
        with open(filename, 'w') as f:
            f.write(f"Latitude: {lat}\nLongitude: {lon}")
        print(f"Coordinates saved to {filename}")
    except Exception as e:
        print(f"Error saving coordinates: {str(e)}")



class WeatherTool(BaseTool):
    name:str = "WeatherTool"
    description:str = "Give info about weather conditions"
    load_dotenv()
    api_key:str = os.getenv('WEATHER_API_KEY')

    def _run(self, city:str) -> str:
        """Fetches weather information for the given location."""

        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        if not self.api_key:
            return str({"error": "Missing API key for weather"})

        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            'q': city,
            'appid': self.api_key,
            'units': 'metric',
            'lang': 'en'
        }

        try:
            response = requests.get(url, params=params)

            if response.status_code == 200:
                data = response.json()

                # Extracting required information
                temp_max = data['main']['temp_max']
                temp_min = data['main']['temp_min']
                wind_speed = data['wind']['speed']
                main_weather = data['weather'][0]['main']
                lat = data['coord']['lat']
                lon = data['coord']['lon']
                save_coordinates_to_file(lat, lon)

                return str({
                    "max_temperature": temp_max,
                    "min_temperature": temp_min,
                    "wind_speed": wind_speed,
                    "main": main_weather
                })
            elif response.status_code == 401:
                self.logger.error("Invalid or inactive API key for weather")
                return str({"error": "Weather API authorization error - check your API key"})
            elif response.status_code == 404:
                self.logger.error(f"Location not found: {city}")
                return str({"error": f"Weather information not found for the city {city}"})
            else:
                error_msg = f"Weather API error ({response.status_code}): {response.text}"
                self.logger.error(error_msg)
                return str({"error": "Failed to fetch weather information"})
        except Exception as e:
            self.logger.error(f"Error while fetching weather: {str(e)}")
            return str({"error": "Error while fetching weather information"})



