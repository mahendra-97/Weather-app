"""
Service for handling weather data storage in GCS only.
"""
import json
import os
from datetime import datetime

from google.cloud import storage

class GCSService:
    """Service for storing and retrieving weather data files in GCS only."""
    def __init__(self, bucket_name=None):
        try:
            self.client = storage.Client()
            self.bucket = self.client.bucket(bucket_name)
        except Exception as e:
            raise RuntimeError(f"Failed to initialize GCS client: {e}")

    def upload_file(self, file_name, data):
        """Upload a JSON file to GCS."""
        print(f"Uploading to GCS bucket: {self.bucket.name}, file: {file_name}")
        blob = self.bucket.blob(file_name)
        blob.upload_from_string(json.dumps(data), content_type='application/json')
        return file_name

    def list_files(self):
        """List all weather data files in GCS."""
        return [blob.name for blob in self.bucket.list_blobs()]

    def get_file_content(self, file_name):
        """Retrieve the content of a weather data file from GCS."""
        blob = self.bucket.blob(file_name)
        try:
            return json.loads(blob.download_as_text())
        except Exception:
            raise FileNotFoundError(f"{file_name} not found in GCS")

# Initialize GCSService once and reuse
_gcs_service = GCSService(os.getenv('GCS_BUCKET_NAME'))

def store_weather_data(weather_data):
    """Store weather data and return the file name used."""
    meta = weather_data.get('meta', {})
    lat = meta.get('latitude', 'NA')
    lon = meta.get('longitude', 'NA')
    start = meta.get('start_date', 'NA')
    end = meta.get('end_date', 'NA')
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    file_name = f"weather_{lat}_{lon}_{start}_{end}_{timestamp}.json"
    return _gcs_service.upload_file(file_name, weather_data)

def list_weather_files():
    """List all weather data files available in GCS."""
    return _gcs_service.list_files()

def get_weather_file_content(file_name):
    """Get the content of a specific weather data file from GCS."""
    return _gcs_service.get_file_content(file_name)