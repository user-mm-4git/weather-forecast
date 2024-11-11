# API Key for WeatherAPI (replace with your actual key)
API_KEY = "639dc520129848b89c2234909240911"
BASE_URL = "http://api.weatherapi.com/v1/forecast.json"

# Zip codes for Hoboken, NJ
ZIPCODES = ["07030","07086"]

FORECAST_RANGE = 3

#Folder Location to save data
DATA_FILES_LOCATION = './weather_forecast_data'
LOG_FILE_LOCATION ='./logs'

#Headers
DAILY_HEADER = [ "zipcode", "date", "maxtemp_f", "mintemp_f", "avgtemp_f",
                "daily_chance_of_rain", "daily_chance_of_snow", "condition.text",
                "condition.icon", "timestamp"]
HOURLY_HEADER = [ "zipcode", "date", "time", "temp_f", "feelslike_f", "heatindex_f",
                "windchill_f", "humidity", "cloud", "chance_of_rain",
                "chance_of_snow", "condition.text", "condition.icon", "timestamp"]