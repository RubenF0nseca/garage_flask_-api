import logging
from flask_restx import Namespace, Resource, abort
from models.employee import Employee
from services.employee_service import get_all_employees, get_employee, create_employee, update_employee, delete_employee
from utils.utils import generate_swagger_model
from werkzeug.exceptions import HTTPException, BadRequest, NotFound

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Namespace for employees
employees_ns = Namespace('employee', description='CRUD operations for managing employees')

# Generate the Swagger model for employees
employee_model = generate_swagger_model(
    api=employees_ns,
    model=Employee,
    exclude_fields=[],
    readonly_fields=['employee_id', 'created_at']
)

# Routes for managing employees
@employees_ns.route('/')
@employees_ns.response(500, 'Internal Server Error')
class EmployeeList(Resource):
    """
    Resource for operations on the collection of employees (GET all, POST new).
    """
    @employees_ns.doc('get_all_employees')
    @employees_ns.marshal_list_with(employee_model)
    def get(self):
        """
        Retrieve all employees.
        :return: List of all employees in dictionary format
        """
        try:
            employees = get_all_employees()
            return employees
        except HTTPException as http_err:
            # Allow HTTP exceptions to propagate as they are
            raise http_err
        except Exception as e:
            # Log and handle unexpected exceptions with a 500 status code
            logger.error(f"Error fetching all employees: {e}")
            employees_ns.abort(500, "Internal Server Error")

    @employees_ns.doc('create_employee')
    @employees_ns.expect(employee_model)
    @employees_ns.marshal_with(employee_model, code=201)
    @employees_ns.response(400, 'Bad Request')
    def post(self):
        """
        Create a new employee.
        :return: Dictionary of the created employee with HTTP 201 status code
        """
        try:
            data = employees_ns.payload
            employee = create_employee(data['name'], data['email'], data['phone'], data['role'], data['hired_date'])
            return employee, 201
        except HTTPException as http_err:
            # Allow HTTP exceptions to propagate as they are
            raise http_err
        except Exception as e:
            # Log and handle unexpected exceptions with a 400 status code
            logger.error(f"Error creating employee: {e}")
            employees_ns.abort(400, "Bad Request")


@employees_ns.route('/<int:employee_id>')
@employees_ns.response(404, 'Employee ID not found')
@employees_ns.response(500, 'Internal Server Error')
@employees_ns.param('employee_id', 'Employee ID')
class Employee(Resource):
    """
    Resource for operations on a single employee (GET, PUT, DELETE).
    """
    @employees_ns.route('/<int:employee_id>')
    class EmployeeResource(Resource):
        @employees_ns.doc('get_employee')
        @employees_ns.marshal_with(employee_model)
        def get(self, employee_id):
            """
            Retrieve a specific employee by ID.
            """
            try:
                # Fetch the employee by ID
                employee = get_employee(employee_id)
                if not employee:
                    # Abort with a 404 status and custom message
                    raise NotFound('My custom message')
                return employee
            # except HTTPException as http_err:
            #     # Allow HTTP exceptions to propagate as they are
            #     raise http_err
            except Exception as e:
                # Log and handle unexpected exceptions with a 500 status code
                logger.error(f"Error fetching employee {employee_id}: {e}")
                abort(500, description="Internal Server Error")

    @employees_ns.doc('update_employee')
    @employees_ns.expect(employee_model)
    @employees_ns.marshal_with(employee_model)
    @employees_ns.response(400, 'Bad Request')
    def put(self, employee_id):
        """
        Update an employee.
        :param employee_id: The ID of the employee
        :return: Dictionary of the updated employee or a 404 error if not found
        """
        try:
            data = employees_ns.payload
            updated_employee = update_employee(employee_id, data['name'], data['email'], data['phone'], data['role'], data['hired_date'])
            if not updated_employee:
                employees_ns.abort(404, f"Employee with ID {employee_id} not found.")
            return updated_employee
        except HTTPException as http_err:
            # Allow HTTP exceptions to propagate as they are
            raise http_err
        except Exception as e:
            # Log and handle unexpected exceptions with a 400 status code
            logger.error(f"Error updating employee {employee_id}: {e}")
            employees_ns.abort(400, "Bad Request")

    @employees_ns.doc('delete_employee')
    def delete(self, employee_id):
        """
        Delete an employee by ID.
        :param employee_id: The ID of the employee
        :return: Empty response body with HTTP 204 status code or a 404 error if not found
        """
        try:
            deleted = delete_employee(employee_id)
            if not deleted:
                employees_ns.abort(404, f"Employee with ID {employee_id} not found.")
            return '', 204
        except HTTPException as http_err:
            # Allow HTTP exceptions to propagate as they are
            raise http_err
        except Exception as e:
            # Log and handle unexpected exceptions with a 500 status code
            logger.error(f"Error deleting employee {employee_id}: {e}")
            employees_ns.abort(500, "Internal Server Error")