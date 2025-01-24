import logging
from datetime import datetime
from models.invoice_item import InvoiceItem
from utils.database import db

logger = logging.getLogger(__name__)

def get_all_invoice_items():
    """
    Retrieve all invoice_items.
    :return: dict: A list of dictionaries containing invoice_item information.
    """
    try:
        invoice_items = InvoiceItem.query.all()
        return [
            {
                "item_id": invoice_item.item_id,
                "cost": invoice_item.cost,
                "description": invoice_item.description,
                "invoice_id": invoice_item.invoice_id,
                "task_id": invoice_item.task_id,
            }
            for invoice_item in invoice_items
        ]
    except Exception as e:
        logger.error(f"Error fetching all invoice_items: {e}")
        return {"error": "Internal Server Error"}

def get_invoice_item(item_id):
    """
    Retrieve an invoice_item by ID.
    :param item_id: The ID of the invoice_item to retrieve.
    :return: dict: A dictionary containing the invoice_item's information or None if not found.
    """
    try:
        invoice_item = InvoiceItem.query.get(item_id)
        if not invoice_item:
            return None
        return {
                "item_id": invoice_item.item_id,
                "cost": invoice_item.cost,
                "description": invoice_item.description,
                "invoice_id": invoice_item.invoice_id,
                "task_id": invoice_item.task_id,
        }
    except Exception as e:
        logger.error(f"Error fetching invoice_item {item_id}: {e}")
        raise

def create_invoice_item(cost, description, invoice_id, task_id):
    """
    Create a new invoice_item.

    """
    try:
        invoice_item = InvoiceItem(
            cost=cost,
            description=description,
            invoice_id=invoice_id,
            task_id=task_id,
        )
        db.session.add(invoice_item)
        db.session.commit()

        return {
                "item_id": invoice_item.item_id,
                "cost": invoice_item.cost,
                "description": invoice_item.description,
                "invoice_id": invoice_item.invoice_id,
                "task_id": invoice_item.task_id,
        }
    except Exception as e:
        logger.error(f"Error creating invoice_item: {e}")
        db.session.rollback()
        return {"error": "Internal Server Error"}, 500

def update_invoice_item(item_id, cost, description, invoice_id, task_id):
    """
    Update an existing invoice_item.

    """
    try:

        invoice_item = InvoiceItem.query.get(item_id)
        if not invoice_item:
            return {"error": f"Invoice_item with ID {item_id} not found."}, 404

        invoice_item.cost = cost
        invoice_item.description = description
        invoice_item.invoice_id = invoice_id
        invoice_item.task_id = task_id

        db.session.commit()
        return {
                "item_id": invoice_item.item_id,
                "cost": invoice_item.cost,
                "description": invoice_item.description,
                "invoice_id": invoice_item.invoice_id,
                "task_id": invoice_item.task_id,
        }
    except Exception as e:
        logger.error(f"Error updating invoice_item {item_id}: {e}")
        db.session.rollback()
        return {"error": "Internal Server Error"}, 500

def delete_invoice_item(item_id):
    """
    Delete an invoice_item.
    :param item_id: The ID of the invoice_item to delete.
    :return: dict: A dictionary confirming the deletion or an error message.
    """
    try:
        invoice_item = InvoiceItem.query.get(item_id)
        if not invoice_item:
            return {"error": f"Invoice_item with ID {item_id} not found."}, 404

        db.session.delete(invoice_item)
        db.session.commit()

        return {"message": f"Invoice_item {item_id} deleted successfully."}, 200
    except Exception as e:
        logger.error(f"Error deleting invoice_item {item_id}: {e}")
        db.session.rollback()
        return {"error": "Internal Server Error"}, 500