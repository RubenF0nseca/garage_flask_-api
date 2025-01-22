from sqlalchemy.orm import relationship
from utils.database import db
from sqlalchemy import ForeignKey
from datetime import datetime


# Model definition for the 'Vehicle' table
class Vehicle(db.Model):
    """
    Represents a vehicle in the database.

    Attributes:
        vehicle_id (int): The primary key for the vehicle table.
        name (str): The name of the vehicle. Must be unique and cannot be null.
        email (str): The email of the vehicle. Cannot be null.
        phone (str): The phone number of the vehicle. Cannot be null.
        address (str): The address of the vehicle. Cannot be null.
        created_at (datetime): Timestamp when the vehicle was created. Defaults to the current time.
    """

    # Define columns for the table
    vehicle_id = db.Column(db.Integer, primary_key=True)  # Unique identifier for each vehicle
    brand = db.Column(db.String(80), nullable=False)
    client_id = db.Column(db.Integer, ForeignKey('client.client_id'), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())  # Auto-generated timestamp
    license_plate = db.Column(db.String(30), nullable=False)
    model = db.Column(db.String(80), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    relationship('Client', back_populates='vehicles')


    def __repr__(self):
        """
        String representation of the Vehicle object.
        Useful for debugging and logging purposes.
        """
        return f"<Vehicle {self.brand}>"