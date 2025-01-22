from flask import Blueprint
from flask_restx import Api

# Main Blueprint for all API routes
api_bp = Blueprint('api', __name__, url_prefix='/api')

# Flask-RESTx Api instance
api = Api(
    api_bp,
    version='1.0',  # API version
    title='Garage API',  # Title displayed in the Swagger documentation
    description='API Swagger documentation',  # Description displayed in the Swagger documentation
    doc='/docs'  # Documentation URL (http://127.0.0.1:5000/api/docs)
)

# Import and register sub-Blueprints (namespaces)
from .client import clients_ns
from .employee import employees_ns
from .setting import settings_ns
from .invoice import invoices_ns
from .vehicle import vehicles_ns

# Add namespaces to the Swagger documentation and API
api.add_namespace(clients_ns, path='/client')  # Routes for client operations
api.add_namespace(employees_ns, path='/employee')  # Routes for employee operations
api.add_namespace(settings_ns, path='/setting')  # Routes for setting operations
api.add_namespace(invoices_ns, path='/invoice')  # Routes for invoice operations
api.add_namespace(vehicles_ns, path='/vehicle')  # Routes for vehicle operations