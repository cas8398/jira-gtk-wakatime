import os
import shelve
import datetime

# Get the user's home directory
home_dir = os.path.expanduser("~")

# Initialize the shelve database file
fix_path_save = os.path.join(home_dir, ".local", "share", "logs_db")


def log_message(log_level, menu_message, message, max_entries=50):
    try:
        # Get current date and time
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Construct a dictionary with log level, date, time, and message
        log_data = {
            "type": log_level,
            "menu": menu_message,
            "datetime": current_time,
            "message": message,
        }

        # Open the shelve database file
        with shelve.open(fix_path_save, writeback=True) as db:
            # Read existing log entries
            existing_logs = db.get("logs", [])

            # Add the new log entry to the list of existing entries
            existing_logs.append(log_data)

            # Keep only the latest entries
            existing_logs = existing_logs[-max_entries:]

            # Store the updated log entries back into the database
            db["logs"] = existing_logs

        # Log message was successfully saved
        return True
    except Exception as e:
        print(f"Error saving log message: {e}")
        return False
