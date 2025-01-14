import logging
from models.employee import Employee
from utils.database import db
from datetime import datetime

logger = logging.getLogger(__name__)

def get_all_employees():
    """
    Retrieve all employees.
    :return: dict: A list of dictionaries containing employee information.
    """
    try:
        employees = Employee.query.all()
        return [{"employee_id": employee.employee_id, "name": employee.name, "email": employee.email, "phone": employee.phone, "role": employee.role, "hired_date": employee.hired_date, "created_at": employee.created_at} for employee in employees]
    except Exception as e:
        logger.error(f"Error fetching all employees: {e}")
        return {"error": "Internal Server Error"}

def get_employee(employee_id):
    """
    Retrieve an employee by ID.
    :param employee_id: The ID of the employee to retrieve.
    :return: dict: A dictionary containing the employee's information or None if not found.
    """
    try:
        # Query the database for the employee by ID
        employee = Employee.query.get(employee_id)
        if not employee:
            return None  # Return None if the employee is not found
        # Return employee data as a dictionary
        return {
            "employee_id": employee.employee_id,
            "name": employee.name,
            "email": employee.email,
            "phone": employee.phone,
            "role": employee.role,
            "hired_date": employee.hired_date,
            "created_at": employee.created_at,
        }
    except Exception as e:
        logger.error(f"Error fetching employee {employee_id}: {e}")
        raise  # Raise the exception to let the API layer handle it

def create_employee(name, email, phone, role, hired_date):
    """
    Create a new employee.
    :param name: The name of the employee.
    :param email: The email of the employee.
    :param phone: The phone number of the employee.
    :param role: The role of the employee.
    :param hired_date: The date the employee was hired.
    :return: dict: A dictionary containing the created employee's information.
    """
    try:
        # Convert hired_date string to datetime.date object
        hired_date_obj = datetime.strptime(hired_date, "%Y-%m-%d").date()
        employee = Employee(name=name, email=email, phone=phone, role=role, hired_date=hired_date_obj)
        db.session.add(employee)  # Save the new employee to the database
        db.session.commit()
        return {"employee_id": employee.employee_id, "name": employee.name, "email": employee.email, "phone": employee.phone, "role": employee.role, "hired_date": employee.hired_date, "created_at": employee.created_at}
    except Exception as e:
        logger.error(f"Error creating employee: {e}")
        return {"error": "Internal Server Error"}


from datetime import datetime


def update_employee(employee_id, name, email, phone, role, hired_date):
    """
    Update an existing employee.
    :param employee_id: The ID of the employee to update.
    :param name: The new name of the employee.
    :param email: The new email of the employee.
    :param phone: The new phone number of the employee.
    :param role: The new role of the employee (mechanic, manager, admin).
    :param hired_date: The new hired date of the employee.
    :return: tuple: A dictionary containing the updated employee's information or an error message and the HTTP status code.
    """
    try:
        # Convert hired_date string to datetime.date object
        hired_date_obj = datetime.strptime(hired_date, "%Y-%m-%d").date()

        # Get the employee from the database
        employee = Employee.query.get(employee_id)
        if not employee:
            return {"error": f"Employee with ID {employee_id} not found."}, 404

        # Update the employee's attributes
        employee.name = name
        employee.email = email
        employee.phone = phone
        employee.role = role
        employee.hired_date = hired_date_obj  # Update hired date

        db.session.commit()  # Commit the transaction

        return {
            "employee_id": employee.employee_id,
            "name": employee.name,
            "email": employee.email,
            "phone": employee.phone,
            "role": employee.role,
            "hired_date": employee.hired_date,
            "created_at": employee.created_at,
        }

    except Exception as e:
        db.session.rollback()  # Rollback on error
        logger.error(f"Error updating employee {employee_id}: {e}")
        return {"error": "Internal Server Error"}, 500

def delete_employee(employee_id):
    """
    Delete an employee.
    :param employee_id: The ID of the employee to delete.
    :return: dict: A dictionary containing the deleted employee's information.
    """
    try:
        employee = Employee.query.get(employee_id)
        if not employee:
            return None
        employee.delete()  # Delete the employee from the database
        return employee
    except Exception as e:
        logger.error(f"Error deleting employee {employee_id}: {e}")
        return {"error": "Internal Server Error"}, 500

