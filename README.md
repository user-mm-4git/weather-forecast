{\rtf1\ansi\ansicpg1252\cocoartf2761
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 ArialMT;}
{\colortbl;\red255\green255\blue255;\red0\green0\blue0;}
{\*\expandedcolortbl;;\cssrgb\c0\c0\c0;}
\margl1440\margr1440\vieww33520\viewh20580\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs36 \cf0 \
# Description\
This Python application fetches weather data from WeatherAPI for specific zip codes and saves the forecast data (both daily and hourly) to CSV files. The application is fully containerized using Docker, making it easy to deploy and execute on any platform.\
\
# Prerequisites\
- Docker\
- Python 3.x (for local testing)\
- pip (for installing dependencies)\
\
# Setup Instructions\
\
# Step 1: Install Docker\
- Download and install Docker from the official website: https://www.docker.com/get-started\
\
#Step 2: Build the Docker Image\
Navigate to the project directory  and run:\
\
```bash\
docker build -t weather-forecast-app .\
\
#Above step will create the image \
\
\
#This will link the local Logs and  weather_forecast_data directories with docker container\
docker run -v $(pwd)/logs:/app/logs -v $(pwd)/weather_forecast_data:/app/weather_forecast_data weather-forecast-app\
\
#Running the test cases\
docker run -v $(pwd)/logs:/app/logs -v $(pwd)/weather_forecast_data:/app/weather_forecast_data -it weather-forecast-app python -m unittest discover -s test\
\
\pard\pardeftab720\partightenfactor0
\cf0 \expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 The program logs are stored in the logs/ directory.\
The forecast data is saved in the weather_forecast_data/ directory,\
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0
\cf0 \kerning1\expnd0\expndtw0 \outl0\strokewidth0 \
\
}