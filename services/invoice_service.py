import logging
from datetime import datetime
from models.invoice import Invoice
from utils.database import db

logger = logging.getLogger(__name__)

def get_all_invoices():
    """
    Retrieve all invoices.
    :return: dict: A list of dictionaries containing invoice information.
    """
    try:
        invoices = Invoice.query.all()
        return [
            {
                "invoice_id": invoice.invoice_id,
                "client_id": invoice.client_id,
                "issued_at": invoice.issued_at,
                "iva": invoice.iva,
                "total": invoice.total,
                "total_with_iva": invoice.total_with_iva,
            }
            for invoice in invoices
        ]
    except Exception as e:
        logger.error(f"Error fetching all invoices: {e}")
        return {"error": "Internal Server Error"}

def get_invoice(invoice_id):
    """
    Retrieve an invoice by ID.
    :param invoice_id: The ID of the invoice to retrieve.
    :return: dict: A dictionary containing the invoice's information or None if not found.
    """
    try:
        invoice = Invoice.query.get(invoice_id)
        if not invoice:
            return None
        return {
            "invoice_id": invoice.invoice_id,
            "client_id": invoice.client_id,
            "issued_at": invoice.issued_at,
            "iva": invoice.iva,
            "total": invoice.total,
            "total_with_iva": invoice.total_with_iva,
        }
    except Exception as e:
        logger.error(f"Error fetching invoice {invoice_id}: {e}")
        raise

def create_invoice(client_id, iva, total, total_with_iva):
    """
    Create a new invoice.
    :param client_id: The ID of the client associated with the invoice.
    :param iva: The IVA (tax) applied to the invoice.
    :param total: The total amount of the invoice before IVA.
    :param total_with_iva: The total amount of the invoice after adding IVA.
    :return: dict: A dictionary containing the newly created invoice's information.
    """
    try:
        invoice = Invoice(
            client_id=client_id,
            iva=iva,
            total=total,
            total_with_iva=total_with_iva,
        )
        db.session.add(invoice)
        db.session.commit()

        return {
            "invoice_id": invoice.invoice_id,
            "client_id": invoice.client_id,
            "issued_at": invoice.issued_at,
            "iva": invoice.iva,
            "total": invoice.total,
            "total_with_iva": invoice.total_with_iva,
        }
    except Exception as e:
        logger.error(f"Error creating invoice: {e}")
        db.session.rollback()
        return {"error": "Internal Server Error"}, 500

def update_invoice(invoice_id, client_id, issued_at, iva, total, total_with_iva):
    """
    Update an existing invoice.
    :param invoice_id: The ID of the invoice to update.
    :param client_id: The new client ID.
    :param issued_at: The new issue date.
    :param iva: The new IVA.
    :param total: The new total before IVA.
    :param total_with_iva: The new total after IVA.
    :return: dict: A dictionary containing the updated invoice's information.
    """
    try:
        issued_at_obj = datetime.strptime(issued_at, "%Y-%m-%d %H:%M:%S")
        invoice = Invoice.query.get(invoice_id)
        if not invoice:
            return {"error": f"Invoice with ID {invoice_id} not found."}, 404

        invoice.client_id = client_id
        invoice.issued_at = issued_at_obj
        invoice.iva = iva
        invoice.total = total
        invoice.total_with_iva = total_with_iva

        db.session.commit()
        return {
            "invoice_id": invoice.invoice_id,
            "client_id": invoice.client_id,
            "issued_at": invoice.issued_at,
            "iva": invoice.iva,
            "total": invoice.total,
            "total_with_iva": invoice.total_with_iva,
        }
    except Exception as e:
        logger.error(f"Error updating invoice {invoice_id}: {e}")
        db.session.rollback()
        return {"error": "Internal Server Error"}, 500

def delete_invoice(invoice_id):
    """
    Delete an invoice.
    :param invoice_id: The ID of the invoice to delete.
    :return: dict: A dictionary confirming the deletion or an error message.
    """
    try:
        invoice = Invoice.query.get(invoice_id)
        if not invoice:
            return {"error": f"Invoice with ID {invoice_id} not found."}, 404

        db.session.delete(invoice)
        db.session.commit()

        return {"message": f"Invoice {invoice_id} deleted successfully."}, 200
    except Exception as e:
        logger.error(f"Error deleting invoice {invoice_id}: {e}")
        db.session.rollback()
        return {"error": "Internal Server Error"}, 500