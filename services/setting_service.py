import logging
from utils.database import db
from models.setting import Setting

logger = logging.getLogger(__name__)

def get_all_settings():
    """
    Retrieve all settings.
    :return: list: A list of dictionaries containing information about all settings.
    """
    try:
        settings = Setting.query.all()  # Retrieve all settings from the database
        return [
            {
                "setting_id": setting.setting_id,
                "key_name": setting.key_name,
                "value": setting.value,
                "updated_at": setting.updated_at,
            }
            for setting in settings
        ]
    except Exception as e:
        logger.error(f"Error fetching all settings: {e}")
        return {"error": "Internal Server Error"}

def get_setting(setting_id):
    """
    Retrieve a setting by ID.
    :param setting_id: The ID of the setting to retrieve.
    :return: dict: A dictionary containing the setting's information or an error message.
    """
    try:
        setting = Setting.query.get(setting_id)
        if not setting:
            return None
        return {
            "setting_id": setting.setting_id,
            "key_name": setting.key_name,
            "value": setting.value,
            "updated_at": setting.updated_at,
        }
    except Exception as e:
        logger.error(f"Error fetching setting {setting_id}: {e}")
        return {"error": "Internal Server Error"}

def create_setting(key_name, value):
    """
    Create a new setting.
    :param key_name: The key name od the setting
    :param value: The value of the setting.
    :return: tuple: A dictionary containing the newly created setting's information and the HTTP status code.
    """
    try:
        setting = Setting(key_name=key_name, value=value)
        db.session.add(setting)
        db.session.commit()
        return {
            "setting_id": setting.setting_id,
            "key_name": setting.key_name,
            "value": setting.value,
            "updated_at": setting.updated_at,
        }
    except Exception as e:
        logger.error(f"Error creating setting: {e}")
        return {"error": "Internal Server Error"}, 500

def update_setting(setting_id, key_name, value):
    """
    Update a setting.
    :param setting_id: The ID of the setting to update.
    :param key_name: The key name od the setting
    :param value: The new value of the setting.
    :return: tuple: A dictionary containing the updated setting's information and the HTTP status code.
    """
    try:
        setting = Setting.query.get(setting_id)
        if not setting:
            return {"error": "Setting not found"}, 404
        setting.key_name = key_name
        setting.value = value
        db.session.commit()
        return {
            "setting_id": setting.setting_id,
            "key_name": setting.key_name,
            "value": setting.value,
            "updated_at": setting.updated_at,
        }, 200
    except Exception as e:
        logger.error(f"Error updating setting {setting_id}: {e}")
        return {"error": "Internal Server Error"}, 500

def delete_setting(setting_id):
    """
    Delete a setting.
    :param setting_id: The ID of the setting to delete.
    :return: tuple: A dictionary containing a success message or an error message and the HTTP status code.
    """
    try:
        setting = Setting.query.get(setting_id)
        if not setting:
            return {"error": "Setting not found"}, 404
        db.session.delete(setting)
        db.session.commit()
        return {"message": "Setting deleted successfully"}, 200
    except Exception as e:
        logger.error(f"Error deleting setting {setting_id}: {e}")
        return {"error": "Internal Server Error"}, 500

