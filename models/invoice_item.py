from sqlalchemy.orm import relationship
from utils.database import db
from sqlalchemy import ForeignKey
from datetime import datetime


# Model definition for the 'Invoice_item' table
class InvoiceItem(db.Model):
    """
    Represents an invoice_item in the database.

    """

    item_id = db.Column(db.Integer, primary_key=True)  # Unique identifier for each invoice_item
    cost = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    invoice_id = db.Column(db.Integer, ForeignKey('invoice.invoice_id'), nullable=False)
    task_id = db.Column(db.Integer, ForeignKey('task.task_id'), nullable=False)

    relationship('Invoice', back_populates='invoice_items')
    relationship('Task', back_populates='invoice_items')

    def __repr__(self):
        """
        String representation of the Invoice_item object.
        Useful for debugging and logging purposes.
        """
        return f"<InvoiceItem {self.item_id}, Cost: {self.cost}, Invoice ID: {self.invoice_id}, Task ID: {self.task_id}>"