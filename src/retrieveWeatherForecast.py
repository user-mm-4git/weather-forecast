import requests
import csv
import os
import logging
from datetime import datetime
import constants


# Set up logging
def setup_log_directory():
    if not os.path.exists(constants.LOG_FILE_LOCATION):
        os.makedirs(constants.LOG_FILE_LOCATION)

    log_filename = os.path.join(constants.LOG_FILE_LOCATION,
                                f"weather_forecast_{datetime.now().strftime('%Y%m%d%H%M%S')}.log")

    logging.basicConfig(
        filename=log_filename,
        level=logging.INFO,  # Log info, warnings, and errors
        format='%(asctime)s - %(levelname)s - %(message)s'
    )


# Function to ensure the data folder exists
def setup_forecast_data_location():
    if not os.path.exists(constants.DATA_FILES_LOCATION):
        os.makedirs(constants.DATA_FILES_LOCATION)
        logging.info(f"Created folder: {constants.DATA_FILES_LOCATION}")


def initialize_data_files(forecastType, header):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    data_filename = f"{constants.DATA_FILES_LOCATION}/{forecastType}_forecast_{timestamp}.csv"
    logging.info(f"{forecastType} forecast data will be saved on {data_filename}")

    try:
        with open(data_filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
        logging.info(f"Data written to {data_filename}")
    except Exception as e:
        logging.error(f"Error writing to {data_filename}: {e}")
    return data_filename


# Function to fetch weather data from WeatherAPI
def get_weather_data(zip_code):
    url = f"{constants.BASE_URL}?key={constants.API_KEY}&q={zip_code}&days=3"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise error for bad responses
        logging.info(f"Successfully fetched data for zip code {zip_code}")
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data for zip code {zip_code}: {e}")
        raise


# Function to extract and save daily forecast data to CSV
def save_daily_forecast(daily_file_name, data, zip_code):
    try:
        with open(daily_file_name, mode='a', newline='') as file:
            writer = csv.writer(file)

            for day in data['forecast']['forecastday']:
                writer.writerow([
                    zip_code,
                    day['date'],
                    day['day']['maxtemp_f'],
                    day['day']['mintemp_f'],
                    day['day']['avgtemp_f'],
                    day['day']['daily_chance_of_rain'],
                    day['day']['daily_chance_of_snow'],
                    day['day']['condition']['text'],
                    day['day']['condition']['icon'],
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ])
        logging.info(f"Daily forecast data saved for zip code {zip_code}")
    except Exception as e:
        logging.error(f"Error saving daily forecast for zip code {zip_code}: {e}")


# Function to extract and save hourly forecast data to CSV
def save_hourly_forecast(hourly_file_name, data, zip_code):
    try:
        with open(hourly_file_name, mode='a', newline='') as file:
            writer = csv.writer(file)

            for day in data['forecast']['forecastday']:
                for hour in day['hour']:
                    writer.writerow([
                        zip_code,
                        day['date'],
                        hour['time'],
                        hour['temp_f'],
                        hour['feelslike_f'],
                        hour['heatindex_f'],
                        hour['windchill_f'],
                        hour['humidity'],
                        hour['cloud'],
                        hour['chance_of_rain'],
                        hour['chance_of_snow'],
                        hour['condition']['text'],
                        hour['condition']['icon'],
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    ])
        logging.info(f"Hourly forecast data saved for zip code {zip_code}")
    except Exception as e:
        logging.error(f"Error saving hourly forecast for zip code {zip_code}: {e}")


# Main function to fetch and save data for each zip code
def main():
    setup_log_directory()
    setup_forecast_data_location()
    daily_file_name = initialize_data_files("daily", constants.DAILY_HEADER)
    hourly_file_name = initialize_data_files("hourly", constants.HOURLY_HEADER)

    for zip_code in constants.ZIPCODES:
        logging.info(f"Fetching weather data for zip code: {zip_code}")
        try:
            data = get_weather_data(zip_code)
            save_daily_forecast(daily_file_name, data, zip_code)
            save_hourly_forecast(hourly_file_name, data, zip_code)
            logging.info(f"Data successfully processed for zip code: {zip_code}")
        except Exception as e:
            logging.error(f"Failed to process data for zip code {zip_code}: {e}")


if __name__ == '__main__':
    main()
