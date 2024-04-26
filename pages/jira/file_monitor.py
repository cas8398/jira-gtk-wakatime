import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


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
    observer.schedule(event_handler, path="pages/jira/json/", recursive=False)
    observer.start()
    # print("File monitor setup complete")
