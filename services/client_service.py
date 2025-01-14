import logging
from utils.database import db
from models.client import Client

logger = logging.getLogger(__name__)

def get_all_clients():
    """
    Retrieve all clients.
    :return: list: A list of dictionaries containing information about all clients.
    """
    try:
        clients = Client.query.all()  # Retrieve all clients from the database
        return [
            {
                "client_id": client.client_id,
                "name": client.name,
                "email": client.email,
                "phone": client.phone,
                "address": client.address,
                "created_at": client.created_at,
            }
            for client in clients
        ]
    except Exception as e:
        logger.error(f"Error fetching all clients: {e}")
        return {"error": "Internal Server Error"}

def get_client(client_id):
    """
    Retrieve a client by ID.
    :param client_id: The ID of the client to retrieve.
    :return: dict: A dictionary containing the client's information or an error message.
    """
    try:
        client = Client.query.get(client_id)
        if not client:
            return None
        return {
            "client_id": client.client_id,
            "name": client.name,
            "email": client.email,
            "phone": client.phone,
            "address": client.address,
            "created_at": client.created_at,
        }
    except Exception as e:
        logger.error(f"Error fetching client {client_id}: {e}")
        return {"error": "Internal Server Error"}

def create_client(name, email, phone, address):
    """
    Create a new client.
    :param name: The name of the client.
    :param email: The email of the client.
    :param phone: The phone number of the client.
    :param address: The address of the client.
    :return: tuple: A dictionary containing the newly created client's information and the HTTP status code.
    """
    try:
        client = Client(name=name, email=email, phone=phone, address=address)
        db.session.add(client)  # Save the new client to the database
        db.session.commit() # Save the new client to the database
        return {
            "client_id": client.client_id,
            "name": client.name,
            "email": client.email,
            "phone": client.phone,
            "address": client.address,
            "created_at": client.created_at,
        }
    except Exception as e:
        logger.error(f"Error creating client: {e}")
        return {"error": "Internal Server Error"}


def update_client(client_id, name, email, phone, address):
    """
    Update an existing client.
    :param client_id: The ID of the client to update.
    :param name: The new name of the client.
    :param email: The new email of the client.
    :param phone: The new phone number of the client.
    :param address: The new address of the client.
    :return: tuple: A dictionary containing the updated client's information or an error message and the HTTP status code.
    """
    try:
        # Find the client by ID
        client = Client.query.get(client_id)

        if not client:
            return None

        # Update the fields if new values are provided (they can be optional)
        client.name = name if name else client.name
        client.email = email if email else client.email
        client.phone = phone if phone else client.phone
        client.address = address if address else client.address

        # Commit the changes to the database
        db.session.commit()
        # Return updated client information
        return {
            "client_id": client.client_id,
            "name": client.name,
            "email": client.email,
            "phone": client.phone,
            "address": client.address,
            "created_at": client.created_at,
        }
    except Exception as e:
        # If an error occurs, rollback the transaction
        db.session.rollback()
        logger.error(f"Error updating client {client_id}: {e}")
        return {"error": "Internal Server Error"}
def delete_client(client_id):
    """
    Delete a client.
    :param client_id: The ID of the client to delete.
    :return: tuple: A message confirming deletion or an error message and the HTTP status code.
    """
    try:
        client = Client.query.get(client_id)
        if not client:
            return None
        # Delete the client
        db.session.delete(client)
        # Commit the deletion
        db.session.commit()
        return client
    except Exception as e:
        logger.error(f"Error deleting client {client_id}: {e}")
        return {"error": "Internal Server Error"}