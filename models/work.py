from sqlalchemy.orm import relationship
from utils.database import db
from sqlalchemy import ForeignKey
from datetime import datetime


# Model definition for the 'Work' table
class Work(db.Model):
    """
    Represents an work in the database.

    """

    work_id = db.Column(db.Integer, primary_key=True)  # Unique identifier for each work
    cost = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())  # Timestamp of work issuance
    description = db.Column(db.String(200), nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(50))
    vehicle_id = db.Column(db.Integer, ForeignKey('vehicle.vehicle_id'), nullable=False)  # Foreign key to 'vehicle'
    relationship('Vehicle', back_populates='works')  # Relationship with the 'Vehicle' model

    def __repr__(self):
        """
        String representation of the Work object.
        Useful for debugging and logging purposes.
        """
        return f"<Work {self.work_id} issued to Vehicle {self.vehicle_id} at {self.created_at}>"