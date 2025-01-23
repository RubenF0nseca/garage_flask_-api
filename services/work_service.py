import logging
from datetime import datetime
from models.work import Work
from utils.database import db

logger = logging.getLogger(__name__)

def get_all_works():
    """
    Retrieve all works.
    :return: dict: A list of dictionaries containing work information.
    """
    try:
        works = Work.query.all()
        return [
            {
                "work_id": work.work_id,
                "cost": work.cost,
                "created_at": work.created_at,
                "description": work.description,
                "end_date": work.end_date,
                "start_date": work.start_date,
                "status": work.status,
                "vehicle_id": work.vehicle_id
            }
            for work in works
        ]
    except Exception as e:
        logger.error(f"Error fetching all works: {e}")
        return {"error": "Internal Server Error"}

def get_work(work_id):
    """
    Retrieve an work by ID.
    :param work_id: The ID of the work to retrieve.
    :return: dict: A dictionary containing the work's information or None if not found.
    """
    try:
        work = Work.query.get(work_id)
        if not work:
            return None
        return {
                "work_id": work.work_id,
                "cost": work.cost,
                "created_at": work.created_at,
                "description": work.description,
                "end_date": work.end_date,
                "start_date": work.start_date,
                "status": work.status,
                "vehicle_id": work.vehicle_id
        }
    except Exception as e:
        logger.error(f"Error fetching work {work_id}: {e}")
        raise

def create_work(cost, description, end_date, start_date, status, vehicle_id):
    """
    Create a new work.

    """
    try:
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

        work = Work(
            cost=cost,
            description=description,
            end_date=end_date,
            start_date=start_date,
            status=status,
            vehicle_id=vehicle_id
        )
        db.session.add(work)
        db.session.commit()

        return {
                "work_id": work.work_id,
                "cost": work.cost,
                "created_at": work.created_at,
                "description": work.description,
                "end_date": work.end_date,
                "start_date": work.start_date,
                "status": work.status,
                "vehicle_id": work.vehicle_id
        }
    except Exception as e:
        logger.error(f"Error creating work: {e}")
        db.session.rollback()
        return {"error": "Internal Server Error"}, 500

def update_work(work_id, cost, description, end_date, start_date, status, vehicle_id):
    """
    Update an existing work.
    """
    try:
        # Buscar o registro existente
        work = Work.query.get(work_id)
        if not work:
            return {"error": f"Work with ID {work_id} not found."}, 404

        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

        work.cost = cost
        work.description = description
        work.end_date = end_date
        work.start_date = start_date
        work.status = status
        work.vehicle_id = vehicle_id

        db.session.commit()
        return {
            "work_id": work.work_id,
            "cost": work.cost,
            "created_at": work.created_at,
            "description": work.description,
            "end_date": work.end_date,
            "start_date": work.start_date,
            "status": work.status,
            "vehicle_id": work.vehicle_id
        }
    except ValueError as ve:
        logger.error(f"Validation error: {ve}")
        return {"error": str(ve)}, 400
    except Exception as e:
        logger.error(f"Error updating work {work_id}: {e}")
        db.session.rollback()
        return {"error": "Internal Server Error"}, 500

def delete_work(work_id):
    """
    Delete an work.
    :param work_id: The ID of the work to delete.
    :return: dict: A dictionary confirming the deletion or an error message.
    """
    try:
        work = Work.query.get(work_id)
        if not work:
            return {"error": f"Work with ID {work_id} not found."}, 404

        db.session.delete(work)
        db.session.commit()

        return {"message": f"Work {work_id} deleted successfully."}, 200
    except Exception as e:
        logger.error(f"Error deleting vehicle {work_id}: {e}")
        db.session.rollback()
        return {"error": "Internal Server Error"}, 500