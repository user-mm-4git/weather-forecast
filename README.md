# Description
This Python application fetches weather data from WeatherAPI for specific zip codes and saves the forecast data (both daily and hourly) to CSV files. The application is fully containerized using Docker, making it easy to deploy and execute on any platform.\
# Prerequisites
- Docker
- Python 3.x (for local testing)
- pip (for installing dependencies)


# Setup Instructions
# Step 1: Install Docker
# Download and install Docker from the official website: https://www.docker.com/get-started


#Step 2: Build the Docker Image
Navigate to the project directory and run
```bash
docker build -t weather-forecast-app .
#Above step will create the image 

#Step 3
#This will link the local Logs and  weather_forecast_data directories with docker container
docker run -v $(pwd)/logs:/app/logs -v $(pwd)/weather_forecast_data:/app/weather_forecast_data weather-forecast-app

#Step 4
#Running the test cases
docker run -v $(pwd)/logs:/app/logs -v $(pwd)/weather_forecast_data:/app/weather_forecast_data -it weather-forecast-app python -m unittest discover -s test\
