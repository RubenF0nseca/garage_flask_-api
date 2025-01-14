import logging
from flask_restx import Namespace, Resource
from werkzeug.exceptions import HTTPException
from services.client_service import (
    get_all_clients,
    get_client,
    create_client,
    update_client,
    delete_client
)
from utils.utils import generate_swagger_model
from models.client import Client


# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Namespace for managing clients
clients_ns = Namespace('client', description='CRUD operations for managing clients')

# Generate the Swagger model for the client resource
client_model = generate_swagger_model(
    api=clients_ns,        # Namespace to associate with the model
    model=Client,          # SQLAlchemy model representing the client resource
    exclude_fields=[],     # No excluded fields in this model
    readonly_fields=['client_id']  # Fields that cannot be modified
)


@clients_ns.route('/')
class ClientList(Resource):
    """
    Handles operations on the collection of clients.
    Supports retrieving all clients (GET) and creating new clients (POST).
    """

    @clients_ns.doc('get_all_clients')
    @clients_ns.marshal_list_with(client_model)
    def get(self):
        """
        Retrieve all clients.
        :return: List of all clients
        """
        try:
            # Fetch all clients from the service layer
            return get_all_clients()
        except HTTPException as http_err:
            # Allow HTTP exceptions to propagate their status codes and messages
            logger.error(f"HTTP error while retrieving clients: {http_err}")
            raise http_err
        except Exception as e:
            # Log error and return a 500 status code
            logger.error(f"Error retrieving clients: {e}")
            clients_ns.abort(500, "An error occurred while retrieving the clients.")

    @clients_ns.doc('create_client')
    @clients_ns.expect(client_model, validate=True)
    @clients_ns.marshal_with(client_model, code=201)
    def post(self):
        """
        Create a new client.
        :return: The created client with HTTP status code 201
        """
        data = clients_ns.payload  # Extract JSON payload
        try:
            # Call the service to create a new client
            return create_client(data["name"],data["email"],data["phone"],data["address"]), 201
        except HTTPException as http_err:
            logger.error(f"HTTP error while creating client: {http_err}")
            raise http_err
        except Exception as e:
            # Log error and return a 500 status code
            logger.error(f"Error creating client: {e}")
            clients_ns.abort(500, "An error occurred while creating the client.")


@clients_ns.route('/<int:client_id>')
@clients_ns.param('client_id', 'The ID of the client')
class Client(Resource):
    """
    Handles operations on a single client.
    Supports retrieving (GET), updating (PUT), and deleting (DELETE) a client.
    """

    @clients_ns.doc('get_client')
    @clients_ns.marshal_with(client_model)
    def get(self, client_id):
        """
        Retrieve a client by ID.
        :param client_id: The ID of the client
        :return: The client details or 404 if not found
        """
        try:
            # Fetch client by ID
            client = get_client(client_id)
            if not client:
                # Return a 404 error if client does not exist
                clients_ns.abort(404, f"Client with ID {client_id} not found.")
            return client
        except HTTPException as http_err:
            logger.error(f"HTTP error while retrieving client with ID {client_id}: {http_err}")
            raise http_err
        except Exception as e:
            # Log error and return a 500 status code
            logger.error(f"Error retrieving client with ID {client_id}: {e}")
            clients_ns.abort(500, "An error occurred while retrieving the client.")

    @clients_ns.doc('update_client')
    @clients_ns.expect(client_model, validate=True)
    @clients_ns.marshal_with(client_model)
    def put(self, client_id):
        """
        Update a client by ID.
        :param client_id: The ID of the client
        :return: The updated client details or 404 if not found
        """
        data = clients_ns.payload  # Extract JSON payload
        try:
            # Call the service to update the client
            client = update_client(client_id, data["name"],data["email"],data["phone"],data["address"])
            if not client:
                # Return a 404 error if client does not exist
                clients_ns.abort(404, f"Client with ID {client_id} not found.")
            return client
        except HTTPException as http_err:
            logger.error(f"HTTP error while updating client with ID {client_id}: {http_err}")
            raise http_err
        except Exception as e:
            # Log error and return a 500 status code
            logger.error(f"Error updating client with ID {client_id}: {e}")
            clients_ns.abort(500, "An error occurred while updating the client.")

    @clients_ns.doc('delete_client')
    @clients_ns.response(204, 'Client successfully deleted')
    def delete(self, client_id):
        """
        Delete a client by ID.
        :param client_id: The ID of the client
        :return: HTTP 204 status code if deleted successfully or 404 if not found
        """
        try:
            # Call the service to delete the client
            client = delete_client(client_id)
            if not client:
                # Return a 404 error if client does not exist
                clients_ns.abort(404, f"Client with ID {client_id} not found.")
            return '', 204  # Return no content with status code 204
        except HTTPException as http_err:
            logger.error(f"HTTP error while deleting client with ID {client_id}: {http_err}")
            raise http_err
        except Exception as e:
            # Log error and return a 500 status code
            logger.error(f"Error deleting client with ID {client_id}: {e}")
            clients_ns.abort(500, "An error occurred while deleting the client.")