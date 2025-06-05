from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from flask_restx import Api
from src.api import api as weather_ns

def create_app():
    app = Flask(__name__)
    
    # Load configuration from config.py
    app.config.from_object('src.config')

    # Set up Flask-RESTX Api for Swagger UI
    api = Api(app, title='Weather Backend API', version='1.0', description='API for weather data storage and retrieval', doc='/swagger/')
    api.add_namespace(weather_ns, path='/')

    @app.route('/')
    def docs_redirect():
        return '<h2>Weather Backend API</h2><p>See <a href="/swagger/">Swagger UI</a></p>'

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=8080, debug=True)