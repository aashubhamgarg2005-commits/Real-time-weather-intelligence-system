import requests
from config.location import districts
from config.config import weather_api_url
from config.logging import logger
import time

def fetch_weather_data():
    """
    Fetches weather data for a given district using the OpenWeatherMap API.

    Args:
        district (dict): A dictionary containing district information including name, latitude, and longitude.

    Returns:
        dict: A dictionary containing the fetched weather data or an error message.
    """
    while True:
            for district in districts:
                try:
                    district_name = district["district"]
                    latitude = district["lattitude"]
                    longitude = district["longitude"]
                    logger.info(f"Fetching weather data for {district_name} (Lat: {latitude}, Lon: {longitude})")
                    response = requests.get(
                    url=weather_api_url,
                    params = {
                    "latitude": district["lattitude"],
                    "longitude": district["longitude"],

                    "current": (
                        "temperature_2m,"
                        "relative_humidity_2m,"
                        "apparent_temperature,"
                        "precipitation,"
                        "rain,"
                        "showers,"
                        "snowfall,"
                        "weather_code,"
                        "cloud_cover,"
                        "pressure_msl,"
                        "wind_speed_10m,"
                        "wind_direction_10m,"
                        "wind_gusts_10m"
                    ),

                    "hourly": (
                        "temperature_2m,"
                        "relative_humidity_2m,"
                        "apparent_temperature,"
                        "precipitation,"
                        "rain,"
                        "showers,"
                        "snowfall,"
                        "weather_code,"
                        "cloud_cover,"
                        "pressure_msl,"
                        "wind_speed_10m,"
                        "wind_direction_10m,"
                        "wind_gusts_10m"
                    ),

                    "timezone": "auto"
                },
                    timeout=30  # Set a timeout for the request
                )
                    
                    response.raise_for_status()
                    data = response.json()
                    weather_data = { "district": district_name,
                                    "latitude": latitude,
                                    "longitude": longitude,
                                        "weather": data }
                    
                    yield weather_data  # Yield the fetched data for the current district
                except Exception as e:
                    logger.error(f"Error fetching weather data for {district['district']}: {e}")
                    continue  # Continue to the next district in case of an error

            logger.info("Completed fetching weather data for all districts. Waiting for the next fetch cycle.")
            logger.info("Sleeping for 600 seconds before the next fetch cycle.")
            time.sleep(600)  # Wait for 600 seconds before the next fetch cycle
