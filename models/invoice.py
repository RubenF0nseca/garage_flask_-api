from sqlalchemy.orm import relationship
from utils.database import db
from sqlalchemy import ForeignKey
from datetime import datetime


# Model definition for the 'Invoice' table
class Invoice(db.Model):
    """
    Represents an invoice in the database.

    Attributes:
        invoice_id (int): The primary key for the invoice table.
        client_id (int): Foreign key referencing the client table.
        issued_at (datetime): Timestamp when the invoice was issued.
        iva (float): The IVA (tax) applied to the invoice.
        total (float): The total amount of the invoice before IVA.
        total_with_iva (float): The total amount of the invoice after adding IVA.
    """

    invoice_id = db.Column(db.Integer, primary_key=True)  # Unique identifier for each invoice
    client_id = db.Column(db.Integer, ForeignKey('client.client_id'), nullable=False)  # Foreign key to 'client'
    issued_at = db.Column(db.DateTime, server_default=db.func.now())  # Timestamp of invoice issuance
    iva = db.Column(db.Float, nullable=False)  # IVA percentage or value
    total = db.Column(db.Float, nullable=False)  # Total amount before IVA
    total_with_iva = db.Column(db.Float, nullable=False)  # Total amount after IVA
    relationship('Client', back_populates='invoices')  # Relationship with the 'Client' model

    def __repr__(self):
        """
        String representation of the Invoice object.
        Useful for debugging and logging purposes.
        """
        return f"<Invoice {self.invoice_id} issued to Client {self.client_id} at {self.issued_at}>"