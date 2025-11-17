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