"""
Service for handling weather data storage in GCS or local filesystem.
"""
import json
import os
from datetime import datetime

USE_GCS = bool(os.getenv('GCS_BUCKET_NAME') and os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))

if USE_GCS:
    from google.cloud import storage

class GCSService:
    """Service for storing and retrieving weather data files in GCS or local storage."""
    def __init__(self, bucket_name=None):
        self.local_dir = os.path.join(os.path.dirname(__file__), '../../local_storage')
        if USE_GCS:
            try:
                self.client = storage.Client()
                self.bucket = self.client.bucket(bucket_name)
            except Exception as e:
                raise RuntimeError(f"Failed to initialize GCS client: {e}")
        else:
            os.makedirs(self.local_dir, exist_ok=True)

    def upload_file(self, file_name, data):
        """Upload a JSON file to GCS or local storage."""
        if USE_GCS:
            blob = self.bucket.blob(file_name)
            blob.upload_from_string(json.dumps(data), content_type='application/json')
            return file_name
        else:
            file_path = os.path.join(self.local_dir, file_name)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f)
            return file_name

    def list_files(self):
        """List all weather data files in GCS or local storage."""
        if USE_GCS:
            return [blob.name for blob in self.bucket.list_blobs()]
        else:
            return [f for f in os.listdir(self.local_dir) if f.endswith('.json')]

    def get_file_content(self, file_name):
        """Retrieve the content of a weather data file from GCS or local storage."""
        if USE_GCS:
            blob = self.bucket.blob(file_name)
            try:
                return json.loads(blob.download_as_text())
            except Exception:
                raise FileNotFoundError(f"{file_name} not found in GCS")
        else:
            file_path = os.path.join(self.local_dir, file_name)
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"{file_name} not found in local storage")
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)

def store_weather_data(weather_data):
    """Store weather data and return the file name used."""
    meta = weather_data.get('meta', {})
    lat = meta.get('latitude', 'NA')
    lon = meta.get('longitude', 'NA')
    start = meta.get('start_date', 'NA')
    end = meta.get('end_date', 'NA')
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    file_name = f"weather_{lat}_{lon}_{start}_{end}_{timestamp}.json"
    gcs = GCSService(os.getenv('GCS_BUCKET_NAME'))
    return gcs.upload_file(file_name, weather_data)

def list_weather_files():
    """List all weather data files available."""
    gcs = GCSService(os.getenv('GCS_BUCKET_NAME'))
    return gcs.list_files()

def get_weather_file_content(file_name):
    """Get the content of a specific weather data file."""
    gcs = GCSService(os.getenv('GCS_BUCKET_NAME'))
    return gcs.get_file_content(file_name)