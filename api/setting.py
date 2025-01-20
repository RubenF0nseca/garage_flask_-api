import logging
from flask_restx import Namespace, Resource
from werkzeug.exceptions import HTTPException
from services.setting_service import (
    get_all_settings,
    get_setting,
    create_setting,
    update_setting,
    delete_setting
)
from utils.utils import generate_swagger_model
from models.setting import Setting

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings_ns = Namespace("setting", description="CRUD operations for managing settings")

# Generate the Swagger model for the setting resource
setting_model = generate_swagger_model(
    api=settings_ns,  # Namespace to associate with the model
    model=Setting,  # SQLAlchemy model representing the setting resource
    exclude_fields=[],  # No excluded fields in this model
    readonly_fields=["setting_id"],  # Fields that cannot be modified
)

@settings_ns.route("/")
class SettingList(Resource):
    """
    Handles operations on the collection of settings.
    Supports retrieving all settings (GET) and creating new settings (POST).
    """

    @settings_ns.doc("get_all_settings")
    @settings_ns.marshal_list_with(setting_model)
    def get(self):
        """
        Retrieve all settings.
        :return: List of all settings
        """
        try:
            # Fetch all settings from the service layer
            return get_all_settings()
        except HTTPException as http_err:
            # Allow HTTP exceptions to propagate their status codes and messages
            logger.error(f"HTTP error while retrieving settings: {http_err}")
            raise http_err
        except Exception as e:
            # Log error and return a 500 status code
            logger.error(f"Error retrieving settings: {e}")
            settings_ns.abort(500, "An error occurred while retrieving the settings.")

    @settings_ns.doc("create_setting")
    @settings_ns.expect(setting_model, validate=True)
    @settings_ns.marshal_with(setting_model, code=201)
    def post(self):
        """
        Create a new setting.
        :return: The newly created setting
        """
        data = settings_ns.payload
        try:
            # Call the service to create a new setting
            key_name = data.get("key_name")
            value = data.get("value")
            return create_setting(key_name, value), 201
        except HTTPException as http_err:
            # Allow HTTP exceptions to propagate their status codes and messages
            logger.error(f"HTTP error while creating a setting: {http_err}")
            raise http_err
        except Exception as e:
            # Log error and return a 500 status code
            logger.error(f"Error creating a setting: {e}")
            settings_ns.abort(500, "An error occurred while creating the setting.")

@settings_ns.route("/<int:setting_id>")
@settings_ns.param("setting_id", "The ID of the setting")

class Setting(Resource):
    """
    Handles operations on a single setting.
    Supports retrieving a setting by ID (GET), updating a setting by ID (PUT), and deleting a setting by ID (DELETE).
    """

    @settings_ns.doc("get_setting")
    @settings_ns.marshal_with(setting_model)
    def get(self, setting_id):
        """
        Retrieve a setting by ID.
        :param setting_id: The ID of the setting to retrieve.
        :return: The setting with the specified ID
        """
        try:
            # Fetch the setting by ID
            setting = get_setting(setting_id)
            if not setting:
                settings_ns.abort(404, f"Setting {setting_id} not found.")
            return setting
        except HTTPException as http_err:
            # Allow HTTP exceptions to propagate their status codes and messages
            logger.error(f"HTTP error while retrieving setting {setting_id}: {http_err}")
            raise http_err
        except Exception as e:
            # Log error and return a 500 status code
            logger.error(f"Error retrieving setting {setting_id}: {e}")
            settings_ns.abort(500, "An error occurred while retrieving the setting.")

    @settings_ns.doc("update_setting")
    @settings_ns.expect(setting_model, validate=True)
    @settings_ns.marshal_with(setting_model)
    def put(self, setting_id):
        """
        Update a setting by ID.
        :param setting_id: The ID of the setting to update.
        :return: The updated setting
        """
        data = settings_ns.payload
        try:
            # Call the service to update the setting
            key_name = data.get("key_name")
            value = data.get("value")
            setting = update_setting(setting_id, key_name, value)
            if not setting:
                settings_ns.abort(404, f"Setting {setting_id} not found.")
            return setting
        except HTTPException as http_err:
            # Allow HTTP exceptions to propagate their status codes and messages
            logger.error(f"HTTP error while updating setting {setting_id}: {http_err}")
            raise http_err
        except Exception as e:
            # Log error and return a 500 status code
            logger.error(f"Error updating setting {setting_id}: {e}")
            settings_ns.abort(500, "An error occurred while updating the setting.")

    @settings_ns.doc("delete_setting")
    @settings_ns.response(204, "Setting successfully deleted ")
    def delete(self, setting_id):
        """
        Delete a setting by ID.
        :param setting_id: The ID of the setting to delete.
        :return: Success message or error message
        """
        try:
            # Call the service to delete the setting
            result, status_code = delete_setting(setting_id)
            return result, status_code
        except HTTPException as http_err:
            logger.error(f"HTTP error while deleting setting {setting_id}: {http_err}")
            raise http_err
        except Exception as e:
            # Log error and return a 500 status code
            logger.error(f"Error deleting setting {setting_id}: {e}")
            settings_ns.abort(500, "An error occurred while deleting the setting.")
