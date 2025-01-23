import logging
from flask_restx import Namespace, Resource
from werkzeug.exceptions import HTTPException
from services.task_service import (
    get_all_tasks,
    get_task,
    create_task,
    update_task,
    delete_task
)
from utils.utils import generate_swagger_model
from models.task import Task

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Namespace for Task
tasks_ns = Namespace("task", description="CRUD operations for managing tasks")

# Generate the Swagger model for the task resource
task_model = generate_swagger_model(
    api=tasks_ns,
    model=Task,
    exclude_fields=[],  # No excluded fields in this model
    readonly_fields=["task_id"],  # Fields that cannot be modified
)

@tasks_ns.route("/")
class TaskList(Resource):
    """
    Handles operations on the collection of tasks.
    Supports retrieving all tasks (GET) and creating new tasks (POST).
    """

    @tasks_ns.doc("get_all_tasks")
    @tasks_ns.marshal_list_with(task_model)
    def get(self):
        """
        Retrieve all tasks.
        :return: List of all tasks.
        """
        try:
            return get_all_tasks()
        except HTTPException as http_err:
            logger.error(f"HTTP error while retrieving tasks: {http_err}")
            raise http_err
        except Exception as e:
            logger.error(f"Error retrieving tasks: {e}")
            tasks_ns.abort(500, "An error occurred while retrieving the tasks.")

    @tasks_ns.doc("create_task")
    @tasks_ns.expect(task_model, validate=True)
    @tasks_ns.marshal_with(task_model, code=201)
    def post(self):
        """
        Create a new task
        :return: The newly created task.
        """
        data = tasks_ns.payload
        try:
            description = data.get("description")
            employee_id = data.get("employee_id")
            start_date = data.get("start_date")
            end_date = data.get("end_date")
            status = data.get("status")
            work_id = data.get("work_id")
            return create_task(description, employee_id, start_date, end_date, status, work_id)
        except HTTPException as http_err:
            logger.error(f"HTTP error while creating task: {http_err}")
            raise http_err
        except Exception as e:
            logger.error(f"Error creating task: {e}")
            tasks_ns.abort(500, "An error occurred while creating the task.")

@tasks_ns.route("/<int:task_id>")
@tasks_ns.param("task_id", "The ID of the task")
class Task(Resource):
    """
    Handles operations on a single task.
    Supports retrieving (GET), updating (PUT), and deleting (DELETE) a task.
    """

    @tasks_ns.doc("get_task")
    @tasks_ns.marshal_with(task_model)
    def get(self, task_id):
        """
        Retrieve a task by ID.
        :param task_id: The ID of the task to retrieve.
        :return: The task with the specified ID.
        """
        try:
            task = get_task(task_id)
            if not task:
                tasks_ns.abort(404, f"Task {task_id} not found.")
            return task
        except HTTPException as http_err:
            logger.error(f"HTTP error while retrieving task {task_id}: {http_err}")
            raise http_err
        except Exception as e:
            logger.error(f"Error retrieving task {task_id}: {e}")
            tasks_ns.abort(500, f"An error occurred while retrieving task {task_id}.")

    @tasks_ns.doc("update_task")
    @tasks_ns.expect(task_model, validate=True)
    @tasks_ns.marshal_with(task_model)
    def put(self, task_id):
        """
        Update a task by ID.
        :param task_id: The ID of the task to update.
        :return: The updated task.
        """
        data = tasks_ns.payload
        try:
            description = data.get("description")
            employee_id = data.get("employee_id")
            start_date = data.get("start_date")
            end_date = data.get("end_date")
            status = data.get("status")
            work_id = data.get("work_id")
            return update_task(task_id, description, employee_id, start_date, end_date, status, work_id)
        except HTTPException as http_err:
            logger.error(f"HTTP error while updating task {task_id}: {http_err}")
            raise http_err
        except Exception as e:
            logger.error(f"Error updating task {task_id}: {e}")
            tasks_ns.abort(500, f"An error occurred while updating task {task_id}.")

    @tasks_ns.doc("delete_task")
    @tasks_ns.response(200, "Invoice successfully deleted")
    @tasks_ns.response(404, "Invoice not found")
    @tasks_ns.response(500, "Internal Server Error")
    def delete(self, task_id):
        """
        Delete a task by ID.
        :param task_id: The ID of the task to delete.
        :return: The result of the deletion operation.
        """
        try:
            result = delete_task(task_id)
            if result:
                return {"message": f"Task {task_id} deleted successfully."}
            else:
                tasks_ns.abort(404, f"Task {task_id} not found.")
        except HTTPException as http_err:
            logger.error(f"HTTP error while deleting task {task_id}: {http_err}")
            raise http_err
        except Exception as e:
            logger.error(f"Error deleting task {task_id}: {e}")
            tasks_ns.abort(500, f"An error occurred while deleting task {task_id}.")
