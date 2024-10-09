# integration/erp_integration.py

import json
import requests
import logging
from app.config import ERP_API_BASE_URL, ERP_CREDENTIALS_PATH, ENABLE_LOGGING, LOG_FILE_PATH, LOG_LEVEL

# Configure logging
if ENABLE_LOGGING:
    logging.basicConfig(filename=LOG_FILE_PATH, 
                        level=getattr(logging, LOG_LEVEL),
                        format='%(asctime)s %(levelname)s %(message)s')


def load_erp_credentials():
    """
    Load ERP credentials from the JSON file.
    
    :return: Dictionary with ERP credentials (e.g., username and API key)
    """
    try:
        with open(ERP_CREDENTIALS_PATH, 'r') as file:
            credentials = json.load(file)
        logging.info("ERP credentials loaded successfully.")
        return credentials
    except Exception as e:
        logging.error(f"Error loading ERP credentials: {e}")
        raise


def authenticate_with_erp():
    """
    Authenticate with the ERP system using stored credentials.
    
    :return: Authentication token if successful, else None
    """
    credentials = load_erp_credentials()
    auth_endpoint = f"{ERP_API_BASE_URL}/auth"
    
    try:
        response = requests.post(auth_endpoint, json={
            "username": credentials["username"],
            "password": credentials["password"]
        })

        if response.status_code == 200:
            auth_token = response.json().get("token")
            logging.info("Authenticated successfully with ERP.")
            return auth_token
        else:
            logging.error(f"Failed to authenticate with ERP: {response.text}")
            return None
    except Exception as e:
        logging.error(f"Error during ERP authentication: {e}")
        raise


def send_data_to_erp(data):
    """
    Send inventory or other relevant data to the ERP system.
    
    :param data: The data to send, usually a dictionary or JSON object.
    :return: True if successful, False otherwise.
    """
    auth_token = authenticate_with_erp()
    if not auth_token:
        logging.error("No authentication token found. Aborting data transmission.")
        return False

    endpoint = f"{ERP_API_BASE_URL}/inventory/update"
    headers = {"Authorization": f"Bearer {auth_token}", "Content-Type": "application/json"}

    try:
        response = requests.post(endpoint, json=data, headers=headers)
        if response.status_code == 200:
            logging.info(f"Data successfully sent to ERP: {data}")
            return True
        else:
            logging.error(f"Failed to send data to ERP: {response.text}")
            return False
    except Exception as e:
        logging.error(f"Error sending data to ERP: {e}")
        raise


def fetch_data_from_erp():
    """
    Fetch inventory or other relevant data from the ERP system.
    
    :return: Data fetched from ERP, usually in JSON format.
    """
    auth_token = authenticate_with_erp()
    if not auth_token:
        logging.error("No authentication token found. Aborting data retrieval.")
        return None

    endpoint = f"{ERP_API_BASE_URL}/inventory/fetch"
    headers = {"Authorization": f"Bearer {auth_token}"}

    try:
        response = requests.get(endpoint, headers=headers)
        if response.status_code == 200:
            data = response.json()
            logging.info("Data successfully fetched from ERP.")
            return data
        else:
            logging.error(f"Failed to fetch data from ERP: {response.text}")
            return None
    except Exception as e:
        logging.error(f"Error fetching data from ERP: {e}")
        raise


def log_message(message, level="INFO"):
    """
    Log a custom message to the log file.

    :param message: The message to log
    :param level: Logging level (e.g., "INFO", "ERROR")
    """
    if ENABLE_LOGGING:
        if hasattr(logging, level):
            getattr(logging, level.lower())(message)
        else:
            logging.info(message)
