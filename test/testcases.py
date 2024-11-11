import sys
import os
import unittest
from unittest.mock import patch, MagicMock
import logging
import requests
import csv
from datetime import datetime

#add the srcdirectory to the Python path so we can import from it
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

#import the module from src folder
import retrieveWeatherForecast as module
import constants

class TestWeatherForecastFunctions(unittest.TestCase):


#testing initialize_data_files function
    @patch('csv.writer')
    @patch('builtins.open', new_callable=MagicMock)
    def test_initialize_data_files(self, mock_open, mock_writer):
        # mock the open function to simulate file opening
        mock_file = MagicMock()
        mock_open.return_value = mock_file
        mock_writer.return_value = MagicMock()

        header = constants.DAILY_HEADER
        forecast_type = "daily"

        # calling the initialize_data_files
        result = module.initialize_data_files(forecast_type, header)

        # Check that the file was created with the correct name
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        expected_filename = f"{constants.DATA_FILES_LOCATION}/{forecast_type}_forecast_{timestamp}.csv"
        self.assertTrue(result.endswith(expected_filename))

        mock_open.assert_called_once_with(expected_filename, mode='w', newline='')
        mock_writer.return_value.writerow.assert_called_once_with(header)

    # testing get_weather_data function
    @patch('requests.get')
    def test_get_weather_data_success(self, mock_get):
    #Mock API response with success
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'forecast': {'forecastday': []}}
        mock_get.return_value = mock_response

        zip_code = "07030"
        data = module.get_weather_data(zip_code)

        #Check the data was fetched correctly
        self.assertEqual(data['forecast']['forecastday'], [])
        mock_get.assert_called_once_with(f"{constants.BASE_URL}?key={constants.API_KEY}&q={zip_code}&days=3")



    #testing test_save_daily_forecast function
    @patch('csv.writer')
    @patch('builtins.open', new_callable=MagicMock)
    def test_save_daily_forecast(self, mock_open, mock_writer):
        #Mock the open function to simulate file opening
        mock_file = MagicMock()
        mock_open.return_value = mock_file
        mock_writer.return_value = MagicMock()

 #sample data
        zip_code = "07030"
        daily_data = {
            'forecast': {
                'forecastday': [{
                    'date': '2024-11-10',
                    'day': {
                        'maxtemp_f': 75.0,
                        'mintemp_f': 55.0,
                        'avgtemp_f': 65.0,
                        'daily_chance_of_rain': 10,
                        'daily_chance_of_snow': 0,
                        'condition': {'text': 'Sunny', 'icon': 'sunny_icon'}
                    }
                }]
            }
        }

        daily_file_name = "daily_forecast.csv"
        module.save_daily_forecast(daily_file_name, daily_data, zip_code)

        #Check whether the data was written correctly to the csv file
        mock_writer.return_value.writerow.assert_called_with([
            zip_code,
            '2024-11-10',
            75.0,
            55.0,
            65.0,
            10,
            0,
            'Sunny',
            'sunny_icon',
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ])

    #Testing save_hourly_forecast function
    @patch('csv.writer')
    @patch('builtins.open', new_callable=MagicMock)
    def test_save_hourly_forecast(self, mock_open, mock_writer):
        # Mock the open function to simulate file opening
        mock_file = MagicMock()
        mock_open.return_value = mock_file
        mock_writer.return_value = MagicMock()

        zip_code = "07030"
        hourly_data = {
            'forecast': {
                'forecastday': [{
                    'date': '2024-11-10',
                    'hour': [{
                        'time': '2024-11-10 10:00',
                        'temp_f': 60.0,
                        'feelslike_f': 59.0,
                        'heatindex_f': 58.0,
                        'windchill_f': 57.0,
                        'humidity': 80,
                        'cloud': 10,
                        'chance_of_rain': 5,
                        'chance_of_snow': 0,
                        'condition': {'text': 'Clear', 'icon': 'clear_icon'}
                    }]
                }]
            }
        }

        hourly_file_name = "hourly_forecast.csv"
        module.save_hourly_forecast(hourly_file_name, hourly_data, zip_code)

        #Checking that data was written correctly to the CSV file
        mock_writer.return_value.writerow.assert_called_with([
            zip_code,
            '2024-11-10',
            '2024-11-10 10:00',
            60.0,
            59.0,
            58.0,
            57.0,
            80,
            10,
            5,
            0,
            'Clear',
            'clear_icon',
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ])

    # Covering the main function
    @patch('retrieveWeatherForecast.setup_log_directory')
    @patch('retrieveWeatherForecast.setup_forecast_data_location')
    @patch('retrieveWeatherForecast.initialize_data_files')
    @patch('retrieveWeatherForecast.get_weather_data')
    @patch('retrieveWeatherForecast.save_daily_forecast')
    @patch('retrieveWeatherForecast.save_hourly_forecast')

    def test_main(self, mock_save_hourly_forecast, mock_save_daily_forecast,
                  mock_get_weather_data, mock_initialize_data_files,
                  mock_setup_forecast_data_location, mock_setup_log_directory):
        #Mocking the dependencies to ensure that the main function runs smoothly
        mock_initialize_data_files.return_value = "daily_forecast.csv", "hourly_forecast.csv"
        mock_get_weather_data.return_value = {'forecast': {'forecastday': []}}
        mock_save_daily_forecast.return_value = None
        mock_save_hourly_forecast.return_value = None

        module.main()


        mock_setup_log_directory.assert_called_once()


        mock_setup_forecast_data_location.assert_called_once()


        mock_initialize_data_files.assert_any_call("daily", constants.DAILY_HEADER)
        mock_initialize_data_files.assert_any_call("hourly", constants.HOURLY_HEADER)


        for zip_code in constants.ZIPCODES:
            mock_get_weather_data.assert_any_call(zip_code)


if __name__ == '__main__':
    unittest.main()
