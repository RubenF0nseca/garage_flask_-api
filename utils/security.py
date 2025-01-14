# Import the necessary functions from the Werkzeug security module
from werkzeug.security import generate_password_hash, check_password_hash


# Function to hash a password
def hash_password(password):
    """
    Hash the given password using Werkzeug's generate_password_hash function.

    :param password: The plain-text password to be hashed.
    :return: A hashed version of the password.
    """
    return generate_password_hash(password)  # Returns a hashed version of the password


# Function to verify if a given password matches the hashed password
def verify_password(hashed_password, password):
    """
    Check if the provided password matches the hashed password.

    :param hashed_password: The hashed password stored in the database.
    :param password: The plain-text password entered by the user.
    :return: True if the password matches, False otherwise.
    """
    return check_password_hash(hashed_password, password)  # Returns True if passwords match