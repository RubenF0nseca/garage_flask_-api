from sqlalchemy.orm import relationship
from utils.database import db
from sqlalchemy import ForeignKey
from datetime import datetime


# Model definition for the 'Task' table
class Task(db.Model):
    """
    Represents a task in the database.

    Attributes:
        task_id (int): The primary key for the task table.
        created_at (datetime): Timestamp when the task was created.
        description (str): Description of the task (required).
        employee_id (int): Foreign key referencing the employee table.
        start_date (date): The date when the task starts (required).
        end_date (date): The date when the task ends.
        status (str): The status of the task.
        work_id (int): Foreign key referencing the work table.
    """

    task_id = db.Column(db.Integer, primary_key=True)  # Unique identifier for each task
    description = db.Column(db.Text, nullable=False)  # Task description
    employee_id = db.Column(db.Integer, ForeignKey('employee.employee_id'), nullable=False)  # Foreign key to 'employee'
    start_date = db.Column(db.Date, nullable=False)  # Task start date
    end_date = db.Column(db.Date)  # Task end date
    status = db.Column(db.Text)  # Task status
    work_id = db.Column(db.Integer, ForeignKey('work.work_id'), nullable=False)  # Foreign key to 'work'
    created_at = db.Column(db.DateTime, server_default=db.func.now())  # Timestamp of task creation

    # Relationships with other models (example)
    employee = relationship('Employee', back_populates='tasks')  # Relationship with 'Employee'
    work = relationship('Work', back_populates='tasks')  # Relationship with 'Work'

    def __repr__(self):
        """
        String representation of the Task object.
        Useful for debugging and logging purposes.
        """
        return f"<Task {self.task_id}: {self.description} (Status: {self.status})>"