import logging
from flask_restx import Namespace, Resource
from werkzeug.exceptions import HTTPException
from services.invoice_service import (
    get_all_invoices,
    get_invoice,
    create_invoice,
    update_invoice,
    delete_invoice
)
from utils.utils import generate_swagger_model
from models.invoice import Invoice

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Namespace for Invoice
invoices_ns = Namespace("invoice", description="CRUD operations for managing invoices")

# Generate the Swagger model for the invoice resource
invoice_model = generate_swagger_model(
    api=invoices_ns,
    model=Invoice,
    exclude_fields=[],  # No excluded fields in this model
    readonly_fields=["invoice_id"],  # Fields that cannot be modified
)

@invoices_ns.route("/")
class InvoiceList(Resource):
    """
    Handles operations on the collection of invoices.
    Supports retrieving all invoices (GET) and creating new invoices (POST).
    """

    @invoices_ns.doc("get_all_invoices")
    @invoices_ns.marshal_list_with(invoice_model)
    def get(self):
        """
        Retrieve all invoices.
        :return: List of all invoices.
        """
        try:
            return get_all_invoices()
        except HTTPException as http_err:
            logger.error(f"HTTP error while retrieving invoices: {http_err}")
            raise http_err
        except Exception as e:
            logger.error(f"Error retrieving invoices: {e}")
            invoices_ns.abort(500, "An error occurred while retrieving the invoices.")

    @invoices_ns.doc("create_invoice")
    @invoices_ns.expect(invoice_model, validate=True)
    @invoices_ns.marshal_with(invoice_model, code=201)
    def post(self):
        """
        Create a new invoice.
        :return: The newly created invoice.
        """
        data = invoices_ns.payload
        try:
            client_id = data.get("client_id")
            issued_at = data.get("issued_at")
            iva = data.get("iva")
            total = data.get("total")
            total_with_iva = data.get("total_with_iva")
            return create_invoice(client_id, issued_at, iva, total, total_with_iva), 201
        except HTTPException as http_err:
            logger.error(f"HTTP error while creating an invoice: {http_err}")
            raise http_err
        except Exception as e:
            logger.error(f"Error creating an invoice: {e}")
            invoices_ns.abort(500, "An error occurred while creating the invoice.")

@invoices_ns.route("/<int:invoice_id>")
@invoices_ns.param("invoice_id", "The ID of the invoice")
class Invoice(Resource):
    """
    Handles operations on a single invoice.
    Supports retrieving an invoice by ID (GET), updating an invoice by ID (PUT), and deleting an invoice by ID (DELETE).
    """

    @invoices_ns.doc("get_invoice")
    @invoices_ns.marshal_with(invoice_model)
    def get(self, invoice_id):
        """
        Retrieve an invoice by ID.
        :param invoice_id: The ID of the invoice to retrieve.
        :return: The invoice with the specified ID.
        """
        try:
            invoice = get_invoice(invoice_id)
            if not invoice:
                invoices_ns.abort(404, f"Invoice {invoice_id} not found.")
            return invoice
        except HTTPException as http_err:
            logger.error(f"HTTP error while retrieving invoice {invoice_id}: {http_err}")
            raise http_err
        except Exception as e:
            logger.error(f"Error retrieving invoice {invoice_id}: {e}")
            invoices_ns.abort(500, "An error occurred while retrieving the invoice.")

    @invoices_ns.doc("update_invoice")
    @invoices_ns.expect(invoice_model, validate=True)
    @invoices_ns.marshal_with(invoice_model)
    def put(self, invoice_id):
        """
        Update an invoice by ID.
        :param invoice_id: The ID of the invoice to update.
        :return: The updated invoice.
        """
        data = invoices_ns.payload
        try:
            client_id = data.get("client_id")
            issued_at = data.get("issued_at")
            iva = data.get("iva")
            total = data.get("total")
            total_with_iva = data.get("total_with_iva")
            invoice = update_invoice(invoice_id, client_id, issued_at, iva, total, total_with_iva)
            if not invoice:
                invoices_ns.abort(404, f"Invoice {invoice_id} not found.")
            return invoice
        except HTTPException as http_err:
            logger.error(f"HTTP error while updating invoice {invoice_id}: {http_err}")
            raise http_err
        except Exception as e:
            logger.error(f"Error updating invoice {invoice_id}: {e}")
            invoices_ns.abort(500, "An error occurred while updating the invoice.")

    @invoices_ns.doc("delete_invoice")
    @invoices_ns.response(204, "Invoice successfully deleted")
    def delete(self, invoice_id):
        """
        Delete an invoice by ID.
        :param invoice_id: The ID of the invoice to delete.
        :return: Success message or error message.
        """
        try:
            result, status_code = delete_invoice(invoice_id)
            return result, status_code
        except HTTPException as http_err:
            logger.error(f"HTTP error while deleting invoice {invoice_id}: {http_err}")
            raise http_err
        except Exception as e:
            logger.error(f"Error deleting invoice {invoice_id}: {e}")
            invoices_ns.abort(500, "An error occurred while deleting the invoice.")