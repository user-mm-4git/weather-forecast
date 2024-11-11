# Use Python 3.9 as the base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables (for logging purposes)
ENV PYTHONUNBUFFERED=1

# Run the main Python script
CMD ["python", "src/retrieveWeatherForecast.py"]
