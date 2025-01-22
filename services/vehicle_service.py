import logging
from datetime import datetime
from utils.database import db
from models.vehicle import Vehicle

logger = logging.getLogger(__name__)

def get_all_vehicles():
    """
    Retrieve all vehicles.
    :return: list: A list of dictionaries containing information about all vehicles.
    """
    try:
        vehicles = Vehicle.query.all()  # Retrieve all vehicles from the database
        return [
            {
                "vehicle_id": vehicle.vehicle_id,
                "brand": vehicle.brand,
                "client_id": vehicle.client_id,
                "created_at": vehicle.created_at,
                "license_plate": vehicle.license_plate,
                "model": vehicle.model,
                "year": vehicle.year,
            }
            for vehicle in vehicles
        ]
    except Exception as e:
        logger.error(f"Error fetching all vehicles: {e}")
        return {"error": "Internal Server Error"}

def get_vehicle(vehicle_id):
    """
    Retrieve a vehicle by ID.
    :param vehicle_id: The ID of the vehicle to retrieve.
    :return: dict: A dictionary containing the vehicle's information or an error message.
    """
    try:
        vehicle = Vehicle.query.get(vehicle_id)
        if not vehicle:
            return None
        return {
                "vehicle_id": vehicle.vehicle_id,
                "brand": vehicle.brand,
                "client_id": vehicle.client_id,
                "created_at": vehicle.created_at,
                "license_plate": vehicle.license_plate,
                "model": vehicle.model,
                "year": vehicle.year,
        }
    except Exception as e:
        logger.error(f"Error fetching vehicle {vehicle_id}: {e}")
        return {"error": "Internal Server Error"}

def create_vehicle(brand, client_id, license_plate, model, year):
    """
    Create a new vehicle.

    :return: tuple: A dictionary containing the newly created vehicle's information and the HTTP status code.
    """
    try:
        vehicle = Vehicle(brand=brand, client_id=client_id, license_plate=license_plate, model=model, year=year)
        db.session.add(vehicle)  # Save the new vehicle to the database
        db.session.commit() # Save the new vehicle to the database
        return {
                "vehicle_id": vehicle.vehicle_id,
                "brand": vehicle.brand,
                "client_id": vehicle.client_id,
                "created_at": vehicle.created_at,
                "license_plate": vehicle.license_plate,
                "model": vehicle.model,
                "year": vehicle.year,
        }
    except Exception as e:
        logger.error(f"Error creating client: {e}")
        return {"error": "Internal Server Error"}


def update_vehicle(vehicle_id, client_id, brand, license_plate, model, year):
    """
    Update an existing vehicle.
    :param vehicle_id: The ID of the vehicle to update.

    :return: tuple: A dictionary containing the updated vehicle's information or an error message and the HTTP status code.
    """
    try:
        # Find the vehicle by ID
        vehicle = Vehicle.query.get(vehicle_id)

        if not vehicle:
            return None

        # Update the fields if new values are provided (they can be optional)
        vehicle.client_id = client_id if client_id else vehicle.client_id
        vehicle.brand = brand if brand else vehicle.brand
        vehicle.license_plate = license_plate if license_plate else vehicle.license_plate
        vehicle.model = model if model else vehicle.model
        vehicle.year = year if year else vehicle.year

        # Commit the changes to the database
        db.session.commit()
        # Return updated vehicle information
        return {
                "vehicle_id": vehicle.vehicle_id,
                "brand": vehicle.brand,
                "client_id": vehicle.client_id,
                "created_at": vehicle.created_at,
                "license_plate": vehicle.license_plate,
                "model": vehicle.model,
                "year": vehicle.year,
        }
    except Exception as e:
        # If an error occurs, rollback the transaction
        db.session.rollback()
        logger.error(f"Error updating vehicle {vehicle_id}: {e}")
        return {"error": "Internal Server Error"}
def delete_vehicle(vehicle_id):
    """
    Delete a vehicle.
    :param vehicle_id: The ID of the vehicle to delete.
    :return: tuple: A message confirming deletion or an error message and the HTTP status code.
    """
    try:
        vehicle = Vehicle.query.get(vehicle_id)
        if not vehicle:
            return None
        # Delete the vehicle
        db.session.delete(vehicle)
        # Commit the deletion
        db.session.commit()
        return vehicle
    except Exception as e:
        logger.error(f"Error deleting vehicle {vehicle_id}: {e}")
        return {"error": "Internal Server Error"}