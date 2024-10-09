# app/__init__.py

"""
Initialization of the app module.

This file is used to initialize the app module and make the necessary imports.
You can also set up global configurations, environment variables, and other
initialization logic needed before running the application.
"""

# Import necessary modules from the app
from .main import run_app  # Import the main function to start the Streamlit app
from .config import APP_TITLE, UPLOAD_FOLDER  # Import global configurations

# Example of initializing a log file or setting environment variables (optional)
import logging
import os

# Ensure the 'uploads' directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Set up logging
logging.basicConfig(
    filename="logs/app_log.log",
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s"
)

logging.info(f"{APP_TITLE} application initialized. Ready to run.")
