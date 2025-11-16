"""
Database scripts module for VekPlay project.
Handles data extraction from VepKar and transformation for VekPlay.
"""

# Standard library imports
import logging
from typing import Optional, Dict, Any

# Third-party imports
import mysql.connector
from mysql.connector import Error
import pandas as pd

# Local imports (relative to this module)
from .config import VEPKAR_DB, VEKPLAY_DB
from .utils.helpers import (
    execute_query,
    save_to_csv,
    save_to_json,
    log_error,
    log_info,
)

# Initialize module-level logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Module constants
DEFAULT_CHUNK_SIZE = 1000  # Chunk size for batch database operations
SUPPORTED_LANGUAGES = ["vep", "krl", "rus", "eng"]  # Language codes used in VekPlay

# Public API of the module (exposed functions/classes)
__all__ = [
    "VEPKAR_DB",
    "VEKPLAY_DB",
    "execute_query",
    "save_to_csv",
    "save_to_json",
    "log_error",
    "log_info",
    "DEFAULT_CHUNK_SIZE",
    "SUPPORTED_LANGUAGES",
]

# Optional: Initialize database connections (lazy-loaded)
_db_connections: Dict[str, Optional[mysql.connector.MySQLConnection]] = {
    "vepkar": None,
    "vekplay": None,
}

def get_db_connection(db_name: str) -> mysql.connector.MySQLConnection:
    """
    Get a database connection (lazy-loaded).

    Args:
        db_name: Name of the database ("vepkar" or "vekplay").

    Returns:
        mysql.connector.MySQLConnection: Active database connection.

    Raises:
        ValueError: If db_name is invalid.
        Error: If connection fails.
    """
    if db_name not in _db_connections:
        raise ValueError(f"Invalid database name: {db_name}. Use 'vepkar' or 'vekplay'.")

    if _db_connections[db_name] is None:
        config = VEPKAR_DB if db_name == "vepkar" else VEKPLAY_DB
        try:
            _db_connections[db_name] = mysql.connector.connect(**config)
            log_info(f"Connected to {db_name} database.")
        except Error as e:
            log_error(f"Failed to connect to {db_name}: {e}")
            raise

    return _db_connections[db_name]

def close_db_connections() -> None:
    """Close all active database connections."""
    for db_name, conn in _db_connections.items():
        if conn is not None:
            conn.close()
            _db_connections[db_name] = None
            log_info(f"Closed connection to {db_name}.")
