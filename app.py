from flask import Flask
from sqlalchemy import false

from api import api_bp  # Import the API blueprint
from config import Config  # Import the configuration class
from utils.database import db  # Import the SQLAlchemy database instance
from utils.utils import configure_logging  # Import the logging configuration function
from errors.errors import register_error_handlers


def create_app():
    """
    Factory function to create and configure the Flask application.
    This function initializes the Flask application, sets up extensions like SQLAlchemy,
    and registers the blueprint for the API routes.
    :return: Configured Flask application instance
    """
    try:
        app = Flask(__name__)
        app.config.from_object(Config)  # Load configuration from the Config class
        register_error_handlers(app)  # Register error handlers for 404 and 500 errors
        db.init_app(app) # Initialize extensions (e.g., SQLAlchemy)
        # Register blueprints (e.g., API routes)
        app.register_blueprint(api_bp)
        return app

    except Exception as e:
        # Log the error and re-raise it to ensure it doesn't get silently ignored
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error during app creation: {e}")
        raise


if __name__ == "__main__":
    # Create the Flask application instance and run it in debug mode
    try:
        #configure_logging()  # Configure the logging system
        app = create_app()
        app.run(debug=False)  # Running in debug mode for development
        #app.run(ERROR_INCLUDE_MESSAGE=False)
    except Exception as e:
        # Catch any exception that occurs while starting the app
        print(f"Failed to start the application: {e}")