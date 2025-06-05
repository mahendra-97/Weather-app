# Weather Backend Service

**Live Demo:** [Swagger UI on Google Cloud Run](https://weather--118898327753.asia-south1.run.app/swagger/)

This project is a backend service that fetches historical weather data from the Open-Meteo Historical Weather API, stores the data in Google Cloud Storage (GCS), and provides an API for listing and retrieving stored weather data files.

## Table of Contents

- [Installation](#installation)
- [Deployment](#deployment)
- [API Documentation (Swagger UI)](#api-documentation-swagger-ui)
- [API Endpoints](#api-endpoints)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/mahendra-97/Weather-app
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

2. Deploy the image to Google Cloud Run (Cloud Build will push the image automatically):
   ```
   gcloud run deploy weather-backend --image gcr.io/weather-task-461909/weather-backend --platform managed --region asia-south1 --allow-unauthenticated --set-env-vars GCS_BUCKET_NAME=open_meteo_weather_bucket,OPEN_METEO_API_URL=https://api.open-meteo.com/v1/forecast
   ```
   Replace `<your-project-id>` and `<your-region>` with your actual GCP project ID and region (e.g., `asia-south1`).

3. Follow the prompts to set the service name, region, and allow unauthenticated invocations if desired.

## API Documentation (Swagger UI)

This service provides an interactive API documentation using **Swagger UI**.

After deploying to Google Cloud Run, you can access the Swagger UI at:

```
https://<your-cloud-run-service-url>/swagger/
```

Replace `<your-cloud-run-service-url>` with the actual URL provided by Cloud Run after deployment (e.g., `https://weather-backend-xxxxxx-uc.a.run.app/swagger/`).

**With Swagger UI, you can:**
- Explore all available API endpoints
- View request and response formats
- Interactively test the API directly from your browser

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