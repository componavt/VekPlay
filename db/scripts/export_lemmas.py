from db.scripts import get_db_connection, save_to_csv, log_info, log_error

def export_data():
    try:
        conn = get_db_connection("vepkar")
        # Ваш код для работы с БД
        log_info("Data exported successfully.")
    except Exception as e:
        log_error(f"Export failed: {e}")
    finally:
        close_db_connections()
