from utils.database import db


# Model definition for the 'Setting' table
class Setting(db.Model):
    """
    Represents a setting in the database.

    Attributes:
        setting_id (int): The primary key for the setting table.
        key_name (str): The key name of the setting. Must be unique and cannot be null.
        value (str): The value of the setting. Cannot be null.
        updated_at (datetime): Timestamp when the setting was last updated. Defaults to the current time.
    """

    # Define columns for the table
    setting_id = db.Column(db.Integer, primary_key=True)  # Unique identifier for each setting
    key_name = db.Column(db.String(80), unique=True, nullable=False)  # Key name, not null
    value = db.Column(db.String(200), nullable=False)  # Setting value, not null
    updated_at = db.Column(db.DateTime, server_default=db.func.now())  # Auto-generated timestamp


    def __repr__(self):
        """
        String representation of the Setting object.
        Useful for debugging and logging purposes.
        """
        return f"<Setting {self.key_name}>"