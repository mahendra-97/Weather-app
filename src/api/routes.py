from http import HTTPStatus
from flask import request
from flask_restx import Namespace, Resource, fields
from src.services.meteo_service import fetch_weather_data
from src.services.gcs_service import store_weather_data, list_weather_files, get_weather_file_content

api = Namespace('Weather', description='Weather Data Operations')

weather_request = api.model('WeatherRequest', {
    'latitude': fields.Float(required=True),
    'longitude': fields.Float(required=True),
    'start_date': fields.String(required=True, example='2024-05-01'),
    'end_date': fields.String(required=True, example='2024-05-03'),
})

def restructure_weather_data(weather_data):
    daily = weather_data['daily']
    dates = daily['time']
    data = {}
    for i, date in enumerate(dates):
        data[date] = {
            "temperature_2m_max": daily['temperature_2m_max'][i],
            "temperature_2m_min": daily['temperature_2m_min'][i],
            "temperature_2m_mean": daily['temperature_2m_mean'][i],
            "apparent_temperature_max": daily['apparent_temperature_max'][i],
            "apparent_temperature_min": daily['apparent_temperature_min'][i],
            "apparent_temperature_mean": daily['apparent_temperature_mean'][i],
        }
    return data

@api.route('/store-weather-data')
class StoreWeatherData(Resource):
    @api.expect(weather_request)
    def post(self):
        data = request.get_json()
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        if not all([latitude, longitude, start_date, end_date]):
            return {'error': 'Missing required parameters'}, HTTPStatus.BAD_REQUEST
        try:
            weather_data = fetch_weather_data(latitude, longitude, start_date, end_date)
            if not weather_data or 'daily' not in weather_data:
                return {'error': 'Failed to fetch weather data'}, HTTPStatus.BAD_GATEWAY
            structured_data = restructure_weather_data(weather_data)
            structured_data['meta'] = {
                'latitude': latitude,
                'longitude': longitude,
                'start_date': start_date,
                'end_date': end_date
            }
            file_name = store_weather_data(structured_data)
            return {'message': 'Weather data stored successfully', 'file_name': file_name}, HTTPStatus.CREATED
        except Exception as e:
            return {'error': str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR

@api.route('/list-weather-files')
class ListWeatherFiles(Resource):
    def get(self):
        try:
            files = list_weather_files()
            return {'message': 'Weather files retrieved successfully', 'files': files}, HTTPStatus.OK
        except Exception as e:
            return {'error': str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR

@api.route('/weather-file-content/<string:file_name>')
class WeatherFileContent(Resource):
    def get(self, file_name):
        try:
            content = get_weather_file_content(file_name)
            if content is None:
                return {'error': 'File not found'}, HTTPStatus.NOT_FOUND
            return {'message': 'Weather file content retrieved successfully', 'data': content}, HTTPStatus.OK    
        except FileNotFoundError:
            return {'error': 'File not found'}, HTTPStatus.NOT_FOUND
        except Exception as e:
            return {'error': str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR