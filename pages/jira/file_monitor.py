import os
import shelve


class JiraFileEventHandler:
    def __init__(self, callback):
        self.callback = callback
        self.previous_db_state = self.read_db_state()

    def read_db_state(self):
        # Get the user's home directory
        home_dir = os.path.expanduser("~")
        # Initialize the shelve database file
        fix_path_save = os.path.join(home_dir, ".local", "share", "jira_issues_db")

        # Open the shelve database file and retrieve its state
        with shelve.open(fix_path_save) as db:
            return dict(db)

    def check_for_changes(self):
        current_db_state = self.read_db_state()
        print("data change")
        if current_db_state != self.previous_db_state:
            self.previous_db_state = current_db_state
            self.callback()


def setup_file_monitor(callback):
    event_handler = JiraFileEventHandler(callback)
    event_handler.check_for_changes()
    print("try watch data")
