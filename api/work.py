import logging
from flask_restx import Namespace, Resource
from werkzeug.exceptions import HTTPException
from services.work_service import (
    get_all_works,
    get_work,
    create_work,
    update_work,
    delete_work
)
from utils.utils import generate_swagger_model
from models.work import Work

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Namespace for Work
works_ns = Namespace("work", description="CRUD operations for managing works")

# Generate the Swagger model for the work resource
work_model = generate_swagger_model(
    api=works_ns,
    model=Work,
    exclude_fields=[],  # No excluded fields in this model
    readonly_fields=["work_id"],  # Fields that cannot be modified
)

@works_ns.route("/")
class WorkList(Resource):
    """
    Handles operations on the collection of works.
    Supports retrieving all works (GET) and creating new works (POST).
    """

    @works_ns.doc("get_all_works")
    @works_ns.marshal_list_with(work_model)
    def get(self):
        """
        Retrieve all works.
        :return: List of all works.
        """
        try:
            return get_all_works()
        except HTTPException as http_err:
            logger.error(f"HTTP error while retrieving works: {http_err}")
            raise http_err
        except Exception as e:
            logger.error(f"Error retrieving works: {e}")
            works_ns.abort(500, "An error occurred while retrieving the works.")

    @works_ns.doc("create_work")
    @works_ns.expect(work_model, validate=True)
    @works_ns.marshal_with(work_model, code=201)
    def post(self):
        """
        Create a new work
        :return: The newly created work.
        """
        data = works_ns.payload
        try:
            cost = data.get("cost")
            description = data.get("description")
            end_date = data.get("end_date")
            start_date = data.get("start_date")
            status = data.get("status")
            vehicle_id = data.get("vehicle_id")


            created_work = create_work(
                cost=cost,
                description=description,
                end_date=end_date,
                start_date=start_date,
                status=status,
                vehicle_id=vehicle_id
            )
            return created_work, 201
        except HTTPException as http_err:
            logger.error(f"HTTP error while creating an work: {http_err}")
            raise http_err
        except Exception as e:
            logger.error(f"Error creating an work: {e}")
            works_ns.abort(500, "An error occurred while creating the work.")

@works_ns.route("/<int:work_id>")
@works_ns.param("work_id", "The ID of the work")
class Work(Resource):
    """
    Handles operations on a single work.
    Supports retrieving an work by ID (GET), updating an work by ID (PUT), and deleting an work by ID (DELETE).
    """

    @works_ns.doc("get_work")
    @works_ns.marshal_with(work_model)
    def get(self, work_id):
        """
        Retrieve an work by ID.
        :param work_id: The ID of the work to retrieve.
        :return: The work with the specified ID.
        """
        try:
            work = get_work(work_id)
            if not work:
                works_ns.abort(404, f"Work {work_id} not found.")
            return work
        except HTTPException as http_err:
            logger.error(f"HTTP error while retrieving work {work_id}: {http_err}")
            raise http_err
        except Exception as e:
            logger.error(f"Error retrieving work {work_id}: {e}")
            works_ns.abort(500, "An error occurred while retrieving the work.")

    @works_ns.doc("update_work")
    @works_ns.expect(work_model, validate=True)
    @works_ns.marshal_with(work_model)
    def put(self, work_id):
        """
        Update an work by ID.
        :param work_id: The ID of the work to update.
        :return: The updated work.
        """
        data = works_ns.payload
        try:
            cost = data.get("cost")
            description = data.get("description")
            end_date = data.get("end_date")
            start_date = data.get("start_date")
            status = data.get("status")
            vehicle_id = data.get("vehicle_id")
            work = update_work(work_id, cost, description, end_date, start_date, status, vehicle_id)
            if not work:
                works_ns.abort(404, f"Work {work_id} not found.")
            return work
        except HTTPException as http_err:
            logger.error(f"HTTP error while updating work {work_id}: {http_err}")
            raise http_err
        except Exception as e:
            logger.error(f"Error updating work {work_id}: {e}")
            works_ns.abort(500, "An error occurred while updating the work.")

    @works_ns.doc("delete_work")
    @works_ns.response(200, "Work successfully deleted")
    @works_ns.response(404, "Work not found")
    @works_ns.response(500, "Internal Server Error")
    def delete(self, work_id):
        """
        Delete an work by ID.
        :param work_id: The ID of the work to delete.
        :return: Success message or error message.
        """
        try:
            result, status_code = delete_work(work_id)
            return result, status_code
        except Exception as e:
            logger.error(f"Unexpected error deleting work {work_id}: {e}")
            works_ns.abort(500, "An unexpected error occurred.")