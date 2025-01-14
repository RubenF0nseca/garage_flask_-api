# utils/swagger.py
from flask_restx import fields
from sqlalchemy import Integer, String, Text, Date, DateTime, Boolean, Float, Numeric
import logging

def generate_swagger_model(api, model, exclude_fields=None, readonly_fields=None):
    """
    Generate a Swagger model from an SQLAlchemy model.

    :param api: Flask-RESTx API instance
    :param model: SQLAlchemy model class
    :param exclude_fields: List of field names to exclude from the Swagger model
    :param readonly_fields: List of field names to mark as read-only
    :return: Flask-RESTx model
    """
    exclude_fields = exclude_fields or []
    readonly_fields = readonly_fields or []

    swagger_model = {}

    for column in model.__table__.columns:
        if column.name in exclude_fields:
            continue

        column_type = type(column.type)
        if column_type in [Integer]:
            field_type = fields.Integer
        elif column_type in [String, Text]:
            field_type = fields.String
        elif column_type == Date:
            field_type = fields.Date
        elif column_type == DateTime:
            field_type = fields.DateTime
        elif column_type == Boolean:
            field_type = fields.Boolean
        elif column_type in [Float, Numeric]:
            field_type = fields.Float
        else:
            # Default to String for unsupported types
            field_type = fields.String

        swagger_field = field_type(description=column.comment or column.name)
        if column.name in readonly_fields or column.primary_key:
            swagger_field.readonly = True

        swagger_model[column.name] = swagger_field

    return api.model(model.__name__, swagger_model)

def configure_logging():
    """
    Configure the logging system for the application.
    Logs messages to both the console and a log file.
    """
    logging.basicConfig(
        level=logging.DEBUG,  # You can adjust the level (DEBUG, INFO, etc.)
        format='%(asctime)s - %(levelname)s - %(message)s',  # Log message format
        handlers=[
            #logging.StreamHandler(),  # Logs to console
            logging.FileHandler('app.log', mode='a')  # Logs to file (app.log)
        ]
    )
