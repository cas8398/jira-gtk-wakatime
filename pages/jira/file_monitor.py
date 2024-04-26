import json
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))


class JiraFileEventHandler(FileSystemEventHandler):
    def __init__(self, callback):
        super().__init__()
        self.callback = callback

    def on_modified(self, event):
        if event.src_path.endswith("jira_issues.json"):
            print("Detected modification in jira_issues.json")
            self.callback()


def setup_file_monitor(callback):
    event_handler = JiraFileEventHandler(callback)
    observer = Observer()
    # Set the icon for the application
    fix_path = os.path.join(current_dir, "json")
    observer.schedule(event_handler, path=fix_path, recursive=False)
    observer.start()
    # print("File monitor setup complete")
