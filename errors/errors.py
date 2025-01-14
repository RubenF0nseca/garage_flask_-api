from flask import jsonify
from werkzeug.exceptions import HTTPException

def register_error_handlers(app):
    """
    Register custom error handlers for the Flask application.
    """

    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        """
        Handle HTTP exceptions with custom responses.
        """
        response = jsonify({"status": "error", "message": e.description})
        response.status_code = e.code
        return response

    @app.errorhandler(Exception)
    def handle_general_exception(e):
        """
        Handle general exceptions (non-HTTP).
        """
        response = jsonify({"status": "error", "message": "An unexpected error occurred."})
        response.status_code = 500
        return response

    @app.errorhandler(404)
    def handle_not_found(e):
        """
        Custom 404 error handler.
        """
        response = jsonify({"status": "error", "message": "Resource not found."})
        response.status_code = 404
        return response