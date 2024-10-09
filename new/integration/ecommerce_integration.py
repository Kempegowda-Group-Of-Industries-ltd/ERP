# integration/ecommerce_integration.py

import json
import requests
import logging
from app.config import ECOMMERCE_API_BASE_URL, ECOMMERCE_CREDENTIALS_PATH, ENABLE_LOGGING, LOG_FILE_PATH, LOG_LEVEL

# Configure logging
if ENABLE_LOGGING:
    logging.basicConfig(filename=LOG_FILE_PATH, 
                        level=getattr(logging, LOG_LEVEL),
                        format='%(asctime)s %(levelname)s %(message)s')


def load_ecommerce_credentials():
    """
    Load eCommerce platform credentials from the JSON file.
    
    :return: Dictionary with eCommerce credentials (e.g., API key or token)
    """
    try:
        with open(ECOMMERCE_CREDENTIALS_PATH, 'r') as file:
            credentials = json.load(file)
        logging.info("eCommerce credentials loaded successfully.")
        return credentials
    except Exception as e:
        logging.error(f"Error loading eCommerce credentials: {e}")
        raise


def authenticate_with_ecommerce():
    """
    Authenticate with the eCommerce platform using stored credentials.
    
    :return: Authentication token if successful, else None
    """
    credentials = load_ecommerce_credentials()
    auth_endpoint = f"{ECOMMERCE_API_BASE_URL}/auth"
    
    try:
        response = requests.post(auth_endpoint, json={
            "api_key": credentials["api_key"],
            "secret_key": credentials["secret_key"]
        })

        if response.status_code == 200:
            auth_token = response.json().get("token")
            logging.info("Authenticated successfully with eCommerce platform.")
            return auth_token
        else:
            logging.error(f"Failed to authenticate with eCommerce platform: {response.text}")
            return None
    except Exception as e:
        logging.error(f"Error during eCommerce authentication: {e}")
        raise


def send_inventory_to_ecommerce(data):
    """
    Send inventory updates to the eCommerce platform.
    
    :param data: The data to send, usually a dictionary or JSON object.
    :return: True if successful, False otherwise.
    """
    auth_token = authenticate_with_ecommerce()
    if not auth_token:
        logging.error("No authentication token found. Aborting inventory transmission.")
        return False

    endpoint = f"{ECOMMERCE_API_BASE_URL}/inventory/update"
    headers = {"Authorization": f"Bearer {auth_token}", "Content-Type": "application/json"}

    try:
        response = requests.post(endpoint, json=data, headers=headers)
        if response.status_code == 200:
            logging.info(f"Inventory data successfully sent to eCommerce: {data}")
            return True
        else:
            logging.error(f"Failed to send inventory data to eCommerce: {response.text}")
            return False
    except Exception as e:
        logging.error(f"Error sending inventory data to eCommerce: {e}")
        raise


def fetch_orders_from_ecommerce():
    """
    Fetch the latest orders from the eCommerce platform.
    
    :return: Data fetched from eCommerce platform, usually in JSON format.
    """
    auth_token = authenticate_with_ecommerce()
    if not auth_token:
        logging.error("No authentication token found. Aborting order retrieval.")
        return None

    endpoint = f"{ECOMMERCE_API_BASE_URL}/orders"
    headers = {"Authorization": f"Bearer {auth_token}"}

    try:
        response = requests.get(endpoint, headers=headers)
        if response.status_code == 200:
            data = response.json()
            logging.info("Orders successfully fetched from eCommerce platform.")
            return data
        else:
            logging.error(f"Failed to fetch orders from eCommerce: {response.text}")
            return None
    except Exception as e:
        logging.error(f"Error fetching orders from eCommerce: {e}")
        raise


def update_order_status(order_id, status):
    """
    Update the status of a specific order in the eCommerce platform.
    
    :param order_id: The ID of the order to update.
    :param status: The new status of the order (e.g., "shipped", "cancelled").
    :return: True if successful, False otherwise.
    """
    auth_token = authenticate_with_ecommerce()
    if not auth_token:
        logging.error("No authentication token found. Aborting order status update.")
        return False

    endpoint = f"{ECOMMERCE_API_BASE_URL}/orders/{order_id}/status"
    headers = {"Authorization": f"Bearer {auth_token}", "Content-Type": "application/json"}

    try:
        response = requests.put(endpoint, json={"status": status}, headers=headers)
        if response.status_code == 200:
            logging.info(f"Order {order_id} status updated to '{status}' on eCommerce platform.")
            return True
        else:
            logging.error(f"Failed to update order status for {order_id}: {response.text}")
            return False
    except Exception as e:
        logging.error(f"Error updating order status for {order_id}: {e}")
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
