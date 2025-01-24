import logging
from flask_restx import Namespace, Resource
from werkzeug.exceptions import HTTPException
from services.invoice_item_service import (
    get_all_invoice_items,
    get_invoice_item,
    create_invoice_item,
    update_invoice_item,
    delete_invoice_item
)
from utils.utils import generate_swagger_model
from models.invoice_item import InvoiceItem

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Namespace for invoice_item
invoice_items_ns = Namespace("invoice_item", description="CRUD operations for managing invoice_items")

# Generate the Swagger model for the invoice_item resource
invoice_item_model = generate_swagger_model(
    api=invoice_items_ns,
    model=InvoiceItem,
    exclude_fields=[],  # No excluded fields in this model
    readonly_fields=["item_id"],  # Fields that cannot be modified
)

@invoice_items_ns.route("/")
class InvoiceItemList(Resource):
    """
    Handles operations on the collection of invoice_items.
    Supports retrieving all invoice_items (GET) and creating new invoice_items (POST).
    """

    @invoice_items_ns.doc("get_all_invoice_items")
    @invoice_items_ns.marshal_list_with(invoice_item_model)
    def get(self):
        """
        Retrieve all invoice_items.
        :return: List of all invoice_items.
        """
        try:
            return get_all_invoice_items()
        except HTTPException as http_err:
            logger.error(f"HTTP error while retrieving invoice_items: {http_err}")
            raise http_err
        except Exception as e:
            logger.error(f"Error retrieving invoice_items: {e}")
            invoice_items_ns.abort(500, "An error occurred while retrieving the invoice_items.")

    @invoice_items_ns.doc("create_invoice_item")
    @invoice_items_ns.expect(invoice_item_model, validate=True)
    @invoice_items_ns.marshal_with(invoice_item_model, code=201)
    def post(self):
        """
        Create a new invoice_item
        :return: The newly created invoice_item.
        """
        data = invoice_items_ns.payload
        try:
            cost = data.get("cost")
            description = data.get("description")
            invoice_id = data.get("invoice_id")
            task_id = data.get("task_id")

            created_invoice_item = create_invoice_item(
                cost=cost,
                description=description,
                invoice_id=invoice_id,
                task_id=task_id
            )
            return created_invoice_item, 201
        except HTTPException as http_err:
            logger.error(f"HTTP error while creating an invoice_item: {http_err}")
            raise http_err
        except Exception as e:
            logger.error(f"Error creating an invoice_item: {e}")
            invoice_items_ns.abort(500, "An error occurred while creating the invoice_item.")

@invoice_items_ns.route("/<int:item_id>")
@invoice_items_ns.param("item_id", "The ID of the invoice_item")
class InvoiceItem(Resource):
    """
    Handles operations on a single invoice_item.
    Supports retrieving an invoice_item by ID (GET), updating an invoice_item by ID (PUT), and deleting an invoice_item by ID (DELETE).
    """

    @invoice_items_ns.doc("get_invoice_item")
    @invoice_items_ns.marshal_with(invoice_item_model)
    def get(self, item_id):
        """
        Retrieve an invoice_item by ID.
        :param item_id: The ID of the invoice_item to retrieve.
        :return: The invoice_item with the specified ID.
        """
        try:
            invoice_item = get_invoice_item(item_id)
            if not invoice_item:
                invoice_items_ns.abort(404, f"Invoice_item {item_id} not found.")
            return invoice_item
        except HTTPException as http_err:
            logger.error(f"HTTP error while retrieving invoice_item {item_id}: {http_err}")
            raise http_err
        except Exception as e:
            logger.error(f"Error retrieving invoice_item {item_id}: {e}")
            invoice_items_ns.abort(500, "An error occurred while retrieving the invoice_item.")

    @invoice_items_ns.doc("update_invoice_item")
    @invoice_items_ns.expect(invoice_item_model, validate=True)
    @invoice_items_ns.marshal_with(invoice_item_model)
    def put(self, item_id):
        """
        Update an invoice_item by ID.
        :param item_id: The ID of the invoice_item to update.
        :return: The updated invoice_item.
        """
        data = invoice_items_ns.payload
        try:
            cost = data.get("cost")
            description = data.get("description")
            invoice_id = data.get("invoice_id")
            task_id = data.get("task_id")
            invoice_item = update_invoice_item(item_id, cost, description, invoice_id, task_id)
            if not invoice_item:
                invoice_items_ns.abort(404, f"Invoice_item {item_id} not found.")
            return invoice_item
        except HTTPException as http_err:
            logger.error(f"HTTP error while updating invoice_item {item_id}: {http_err}")
            raise http_err
        except Exception as e:
            logger.error(f"Error updating invoice_item {item_id}: {e}")
            invoice_items_ns.abort(500, "An error occurred while updating the invoice_item.")

    @invoice_items_ns.doc("delete_invoice_item")
    @invoice_items_ns.response(200, "Invoice_item successfully deleted")
    @invoice_items_ns.response(404, "Invoice_item not found")
    @invoice_items_ns.response(500, "Internal Server Error")
    def delete(self, item_id):
        """
        Delete an invoice_item by ID.
        :param item_id: The ID of the invoice_item to delete.
        :return: Success message or error message.
        """
        try:
            result, status_code = delete_invoice_item(item_id)
            return result, status_code
        except Exception as e:
            logger.error(f"Unexpected error deleting invoice_item {item_id}: {e}")
            invoice_items_ns.abort(500, "An unexpected error occurred.")