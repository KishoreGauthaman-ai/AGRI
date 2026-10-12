import requests
import os
from dotenv import load_dotenv

load_dotenv()

class WeatherAPI:
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
    API_KEY = os.getenv("OPENWEATHER_API_KEY")

    @staticmethod
    def get_weather(city):
        if not WeatherAPI.API_KEY or WeatherAPI.API_KEY == "your_openweather_api_key_here":
            # Mock data for demonstration if key is missing
            return {
                "temp": 28,
                "humidity": 65,
                "wind_speed": 12,
                "condition": "Cloudy (Mock Data)",
                "icon": "weather-cloudy"
            }

        try:
            params = {
                "q": city,
                "appid": WeatherAPI.API_KEY,
                "units": "metric"
            }
            response = requests.get(WeatherAPI.BASE_URL, params=params)
            data = response.json()
           
            if response.status_code == 200:
                weather_condition = data['weather'][0]['main']
                icon_map = {
                    "Clear": "weather-sunny",
                    "Clouds": "weather-cloudy",
                    "Rain": "weather-rainy",
                    "Drizzle": "weather-partly-rainy",
                    "Thunderstorm": "weather-lightning",
                    "Snow": "weather-snowy",
                    "Mist": "weather-fog",
                    "Smoke": "weather-fog",
                    "Haze": "weather-hazy",
                    "Dust": "weather-hazy",
                    "Fog": "weather-fog",
                    "Sand": "weather-hazy",
                    "Ash": "weather-hazy",
                    "Squall": "weather-windy",
                    "Tornado": "weather-hurricane"
                }
                
                return {
                    "temp": data['main']['temp'],
                    "humidity": data['main']['humidity'],
                    "wind_speed": data['wind']['speed'],
                    "condition": data['weather'][0]['description'].capitalize(),
                    "icon": icon_map.get(weather_condition, "weather-cloudy"),
                    'feels_like': data['main']['feels_like'],
                    'sea_level': data['main']['sea_level'], 
                    'coord': data['coord'],
                    'data': data
                }
            else:
                return {"error": data.get("message", "Unknown error")}
        except Exception as e:
            return {"error": str(e)}
