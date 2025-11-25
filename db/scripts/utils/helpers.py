import pandas as pd
import mysql.connector
from mysql.connector import Error
import os

def execute_query(connection, query, params=None):
    """Execute SQL query with parameters"""
    cursor = connection.cursor()
    try:
        cursor.execute(query, params)
        connection.commit()
        return True
    except Error as e:
        print(f"Query execution error: {e}")
        connection.rollback()
        return False
    finally:
        cursor.close()

def save_to_csv(dataframe, filepath):
    """Save DataFrame to CSV file"""
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    dataframe.to_csv(filepath, index=False)


def save_to_json(data, filepath):
    """Save data to JSON file"""
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    import json
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def log_error(message):
    """Log error message"""
    import logging
    logger = logging.getLogger(__name__)
    logger.error(message)


def log_info(message):
    """Log info message"""
    import logging
    logger = logging.getLogger(__name__)
    logger.info(message)