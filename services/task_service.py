import logging
from datetime import datetime
from models.task import Task
from utils.database import db

logger = logging.getLogger(__name__)

def get_all_tasks():
    """
    Retrieve all tasks.
    :return: dict: A list of dictionaries containing task information.
    """
    try:
        tasks = Task.query.all()
        return [
            {
                "task_id": task.task_id,
                "created_at": task.created_at,
                "description": task.description,
                "employee_id": task.employee_id,
                "start_date": task.start_date,
                "end_date": task.end_date,
                "status": task.status,
                "work_id": task.work_id,
            }
            for task in tasks
        ]
    except Exception as e:
        logger.error(f"Error fetching all tasks: {e}")
        return {"error": "Internal Server Error"}

def get_task(task_id):
    """
    Retrieve a task by ID.
    :param task_id: The ID of the task to retrieve.
    :return: dict: A dictionary containing the task's information or None if not found.
    """
    try:
        task = Task.query.get(task_id)
        if not task:
            return None
        return {
            "task_id": task.task_id,
            "created_at": task.created_at,
            "description": task.description,
            "employee_id": task.employee_id,
            "start_date": task.start_date,
            "end_date": task.end_date,
            "status": task.status,
            "work_id": task.work_id,
        }
    except Exception as e:
        logger.error(f"Error fetching task {task_id}: {e}")
        raise

def create_task(description, employee_id, start_date, end_date, status, work_id):
    """
    Create a new task.
    :param description: The description of the task.
    :param employee_id: The ID of the employee assigned to the task.
    :param start_date: The start date of the task.
    :param end_date: The end date of the task.
    :param status: The status of the task.
    :param work_id: The ID of the work associated with the task.
    :return: dict: A dictionary containing the newly created task's information.
    """
    try:
        new_task = Task(
            description=description,
            employee_id=employee_id,
            start_date=start_date,
            end_date=end_date,
            status=status,
            work_id=work_id,
        )
        db.session.add(new_task)
        db.session.commit()
        return {
            "task_id": new_task.task_id,
            "created_at": new_task.created_at,
            "description": new_task.description,
            "employee_id": new_task.employee_id,
            "start_date": new_task.start_date,
            "end_date": new_task.end_date,
            "status": new_task.status,
            "work_id": new_task.work_id,
        }
    except Exception as e:
        logger.error(f"Error creating task: {e}")
        db.session.rollback()
        return {"error": "Internal Server Error"}

def update_task(task_id, description, employee_id, start_date, end_date, status, work_id):
    """
    Update an existing task.
    :param task_id: The ID of the task to update.
    :param description: The new description of the task.
    :param employee_id: The new employee ID.
    :param start_date: The new start date.
    :param end_date: The new end date.
    :param status: The new status.
    :param work_id: The new work ID.
    :return: dict: A dictionary containing the updated task's information.
    """
    try:
        task = Task.query.get(task_id)
        if not task:
            return None
        task.description = description
        task.employee_id = employee_id
        task.start_date = start_date
        task.end_date = end_date
        task.status = status
        task.work_id = work_id
        db.session.commit()
        return {
            "task_id": task.task_id,
            "created_at": task.created_at,
            "description": task.description,
            "employee_id": task.employee_id,
            "start_date": task.start_date,
            "end_date": task.end_date,
            "status": task.status,
            "work_id": task.work_id,
        }
    except Exception as e:
        logger.error(f"Error updating task {task_id}: {e}")
        db.session.rollback()
        return {"error": "Internal Server Error"}

def delete_task(task_id):
    """
    Delete a task by ID.
    :param task_id: The ID of the task to delete.
    :return: dict: A dictionary containing a success message or an error message.
    """
    try:
        task = Task.query.get(task_id)
        if not task:
            return None
        db.session.delete(task)
        db.session.commit()
        return {"message": "Task successfully deleted"}
    except Exception as e:
        logger.error(f"Error deleting task {task_id}: {e}")
        db.session.rollback()
        return {"error": "Internal Server Error"}