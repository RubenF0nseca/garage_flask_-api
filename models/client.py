from utils.database import db


# Model definition for the 'Client' table
class Client(db.Model):
    """
    Represents a client in the database.

    Attributes:
        client_id (int): The primary key for the client table.
        name (str): The name of the client. Must be unique and cannot be null.
        email (str): The email of the client. Cannot be null.
        phone (str): The phone number of the client. Cannot be null.
        address (str): The address of the client. Cannot be null.
        created_at (datetime): Timestamp when the client was created. Defaults to the current time.
    """

    # Define columns for the table
    client_id = db.Column(db.Integer, primary_key=True)  # Unique identifier for each client
    name = db.Column(db.String(80), unique=True, nullable=False)  # Client name, must be unique
    email = db.Column(db.String(200), nullable=False)  # Client email
    phone = db.Column(db.String(20), nullable=False)  # Client phone number
    address = db.Column(db.String(200), nullable=False)  # Client address
    created_at = db.Column(db.DateTime, server_default=db.func.now())  # Auto-generated timestamp

    def __repr__(self):
        """
        String representation of the Client object.
        Useful for debugging and logging purposes.
        """
        return f"<Client {self.name}>"