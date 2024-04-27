import requests
from requests.auth import HTTPBasicAuth
from gi.repository import Gtk
import json
import shelve
import os
from .jira_done import change_issue_done
from .logging import log_message


# Get the current directory
def load_setting_data():
    # Get the user's home directory
    home_dir = os.path.expanduser("~")

    # Initialize the shelve database file path
    fix_path_save = os.path.join(home_dir, ".local", "share", "jira_settings_db")

    try:
        # Open the shelve database file
        with shelve.open(fix_path_save) as db:
            # Create a dictionary-like object to hold the settings data
            settings_data = {
                "accountId": db.get("accountId"),
                "id_done": db.get("id_done"),
                "default_desc": db.get("default_desc"),
                "email": db.get("email"),
                "jira_url": db.get("jira_url"),
                "jira_token": db.get("jira_token"),
            }
            return settings_data
    except Exception as e:
        print(f"Error accessing shelve database: {e}")
        return None


def change_issue_desc(issue_key, issue_title, update):
    # Load data from the file
    data = load_setting_data()

    # Extract the value corresponding
    jira_url = data["jira_url"]
    jira_email = data["email"]
    jira_token = data["jira_token"]

    # Start API
    url = f"https://{jira_url}/rest/api/2/issue/" + issue_key
    auth = HTTPBasicAuth(jira_email, jira_token)

    headers = {"Accept": "application/json", "Content-Type": "application/json"}

    # Payload to update the issue status to "Done"
    payload = json.dumps(
        {
            "update": {
                "description": [{"set": update}],
            },
        }
    )

    try:
        # Send PUT request to update the issue status
        response = requests.request(
            "PUT", url, data=payload, headers=headers, auth=auth
        )
        response.raise_for_status()  # Raise an exception for HTTP errors
        print("Issue desc updated successfully.")
        log_message(
            log_level="info",
            menu_message="description issue",
            message=f"{issue_key} _ status : Success",
        )

        # run change done
        change_issue_done(issue_key, issue_title)

    except requests.HTTPError as e:
        print(f"Failed to update issue status: {e}")
        log_message(
            log_level="error",
            menu_message="description issue",
            message=f"{issue_key} _ status : " + str(e),
        )
        # alert
        dialog = Gtk.MessageDialog(
            flags=0,
            message_type=Gtk.MessageType.OTHER,
            buttons=Gtk.ButtonsType.OK,
            text="Error Description \n" + "status: : " + str(e),
        )
        dialog.run()
        dialog.destroy()


# Example usage: Change status of issue with key "ABC-123" to "Done"
# change_issue_status("SKM-13", "Super DUper after")
