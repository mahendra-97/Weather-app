# Weather Backend Service

This project is a backend service that fetches historical weather data from the Open-Meteo Historical Weather API, stores the data in Google Cloud Storage (GCS), and provides an API for listing and retrieving stored weather data files.

## Table of Contents

- [Installation](#installation)
- [Deployment](#deployment)
- [API Endpoints](#api-endpoints)

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd weather-backend
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Deployment

To deploy the application on Google Cloud Run, follow these steps:

1. Build the Docker image:
   ```
   docker build -t gcr.io/<your-project-id>/weather-backend .
   ```

2. Push the Docker image to Google Container Registry:
   ```
   docker push gcr.io/<your-project-id>/weather-backend
   ```

3. Deploy the image to Google Cloud Run:
   ```
   gcloud run deploy weather-backend --image gcr.io/<your-project-id>/weather-backend --platform managed
   ```

4. Follow the prompts to set the service name, region, and allow unauthenticated invocations if desired.

## API Endpoints

### POST /store-weather-data

- **Description**: Fetch historical weather data and store it in GCS.
- **Request Body**:
  ```json
  {
    "latitude": <float>,
    "longitude": <float>,
    "start_date": "<YYYY-MM-DD>",
    "end_date": "<YYYY-MM-DD>"
  }
  ```
- **Response**: Success message and file name.

### GET /list-weather-files

- **Description**: List all weather data files stored in GCS.
- **Response**: JSON array of file names.

### GET /weather-file-content/<file_name>

- **Description**: Fetch and display the content of a specific JSON file stored in GCS.
- **Response**: JSON content of the specified file.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.