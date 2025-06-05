import os

class Config:
    """Configuration settings for the application."""
    OPEN_METEO_API_URL = os.getenv('OPEN_METEO_API_URL', 'https://api.open-meteo.com/v1/forecast')
    GCS_BUCKET_NAME = os.getenv('GCS_BUCKET_NAME', 'open_meteo_weather_bucket')
    GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', 'path/to/your/service-account-file.json')
    JSON_FILE_PREFIX = 'weather_data_'  # Prefix for stored JSON files
    JSON_FILE_EXTENSION = '.json'  # Extension for stored JSON files
    DEFAULT_LATITUDE = 0.0  # Default latitude if not provided
    DEFAULT_LONGITUDE = 0.0  # Default longitude if not provided
    DEFAULT_START_DATE = '2020-01-01'  # Default start date if not provided
    DEFAULT_END_DATE = '2020-01-31'  # Default end date if not provided