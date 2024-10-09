# app/utils.py

import os
import pandas as pd
import logging
from app.config import UPLOAD_FOLDER, ENABLE_LOGGING, LOG_FILE_PATH, LOG_LEVEL

# Configure logging
if ENABLE_LOGGING:
    logging.basicConfig(filename=LOG_FILE_PATH, 
                        level=getattr(logging, LOG_LEVEL),
                        format='%(asctime)s %(levelname)s %(message)s')


def save_uploaded_file(uploaded_file):
    """
    Save an uploaded file to the specified upload directory.

    :param uploaded_file: Streamlit uploaded file object
    :return: Full file path where the file was saved
    """
    # Ensure the upload folder exists
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    # Save the file
    file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    logging.info(f"File {uploaded_file.name} saved to {file_path}.")
    return file_path


def load_csv_file(file_path):
    """
    Load a CSV file into a Pandas DataFrame.

    :param file_path: Full path to the CSV file
    :return: Pandas DataFrame with the CSV contents
    """
    try:
        df = pd.read_csv(file_path)
        logging.info(f"CSV file loaded from {file_path}.")
        return df
    except Exception as e:
        logging.error(f"Error loading CSV file from {file_path}: {e}")
        raise


def get_basic_statistics(df):
    """
    Calculate basic statistics for a DataFrame.

    :param df: Pandas DataFrame
    :return: DataFrame with basic statistics (describe)
    """
    try:
        stats = df.describe()
        logging.info("Basic statistics generated.")
        return stats
    except Exception as e:
        logging.error(f"Error generating statistics: {e}")
        raise


def filter_data_by_category(df, category):
    """
    Filter the DataFrame by a specific category.

    :param df: Pandas DataFrame
    :param category: The category to filter by
    :return: Filtered DataFrame
    """
    try:
        filtered_df = df[df["Category"] == category]
        logging.info(f"Data filtered by category: {category}.")
        return filtered_df
    except Exception as e:
        logging.error(f"Error filtering data by category {category}: {e}")
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
