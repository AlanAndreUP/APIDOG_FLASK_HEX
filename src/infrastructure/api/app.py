import os
from flask import Flask
from flask_cors import CORS

from src.application.services.dog_service import DogService
from src.infrastructure.api.controllers.dog_controller import DogController
from src.infrastructure.api.routes.dog_routes import register_routes
from src.infrastructure.external.dog_api.client import DogAPIClient

def create_app() -> Flask:
    """Creates and configures the Flask application."""
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": ["http://localhost:3000"]}})
    dog_repository = DogAPIClient()
    dog_service = DogService(dog_repository)
    dog_controller = DogController(dog_service)
    register_routes(app, dog_controller)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True) 