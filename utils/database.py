# Import the necessary modules from Flask and SQLAlchemy
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

# Base class for SQLAlchemy models. All model classes will inherit from this class.
# This allows SQLAlchemy to recognize them as models and interact with the database.
class Base(DeclarativeBase):
  pass  # Placeholder for model classes, no extra functionality is added here.

# Create an instance of SQLAlchemy to manage database interactions
# The 'model_class=Base' argument tells SQLAlchemy that all models will inherit from the Base class
db = SQLAlchemy(model_class=Base)

