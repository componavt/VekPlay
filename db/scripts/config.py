import os
from dotenv import load_dotenv

load_dotenv()

VEPKAR_DB = {
    "host": os.getenv("VEPKAR_DB_HOST", "localhost"),
    "user": os.getenv("VEPKAR_DB_USER", "user"),
    "password": os.getenv("VEPKAR_DB_PASSWORD", "password"),
    "database": os.getenv("VEPKAR_DB_NAME", "vepkar"),
}

VEKPLAY_DB = {
    "host": os.getenv("VEKPLAY_DB_HOST", "localhost"),
    "user": os.getenv("VEKPLAY_DB_USER", "user"),
    "password": os.getenv("VEKPLAY_DB_PASSWORD", "password"),
    "database": os.getenv("VEKPLAY_DB_NAME", "vekplay"),
}
