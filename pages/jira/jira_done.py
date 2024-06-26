import requests
from requests.auth import HTTPBasicAuth
import json
import shelve
import os
from gi.repository import Gtk
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


def remove_issue(issue_key):
    # Get the user's home directory
    home_dir = os.path.expanduser("~")

    # Initialize the shelve database file
    fix_path_save = os.path.join(home_dir, ".local", "share", "jira_issues_db")

    try:
        # Open the shelve database file
        with shelve.open(fix_path_save, writeback=True) as db:
            # Get the list of selected issues
            selected_issues = db.get("selected_issues", [])

            # Filter out the item with the specified ID
            filtered_issues = [
                issue for issue in selected_issues if issue.get("id") != str(issue_key)
            ]

            # Update the database with the filtered issues
            db["selected_issues"] = filtered_issues

            print(f"Issue with key {issue_key} removed successfully.")
            return True
    except Exception as e:
        print(f"Error removing issue: {e}")
        return False


def change_issue_done(issue_key, issue_title):
    # Load data from the file
    data = load_setting_data()

    # Extract the value corresponding
    jira_url = data["jira_url"]
    jira_email = data["email"]
    jira_token = data["jira_token"]
    jira_id_done = data["id_done"]

    # Start API
    url = f"https://{jira_url}/rest/api/2/issue/" + issue_key + "/transitions"
    auth = HTTPBasicAuth(jira_email, jira_token)

    headers = {"Accept": "application/json", "Content-Type": "application/json"}

    # Payload to update the issue status to "Done"
    payload = json.dumps({"transition": {"id": jira_id_done}})
    try:
        # Send PUT request to update the issue status
        response = requests.request(
            "POST", url, data=payload, headers=headers, auth=auth
        )
        response.raise_for_status()  # Raise an exception for HTTP errors
        print("Issue done updated successfully.")
        log_message(
            log_level="info",
            menu_message="finish issue",
            message=f"{issue_key} _ status : Success",
        )

        # remove issue
        remove_issue(issue_key)

        dialog = Gtk.MessageDialog(
            flags=0,
            message_type=Gtk.MessageType.OTHER,
            buttons=Gtk.ButtonsType.OK,
            text="Success ! \n" + "issues: : " + issue_title,
        )
        # Connect a callback function to handle the response
        # dialog.connect("response", on_dialog_response)

        dialog.run()
        dialog.destroy()

    except requests.HTTPError as e:
        print(f"Failed to update issue status: {e}")
        log_message(
            log_level="error",
            menu_message="finish issue",
            message=f"{issue_key} _ status : " + str(e),
        )

        # alert
        dialog = Gtk.MessageDialog(
            flags=0,
            message_type=Gtk.MessageType.OTHER,
            buttons=Gtk.ButtonsType.OK,
            text="Error Check Done \n" + "status: : " + str(e),
        )
        dialog.run()
        dialog.destroy()


""""
    def on_dialog_response(self, dialog, response_id):
    if response_id == Gtk.ResponseType.OK:
        # Call the reload_data function here
        print("reloaded.")
"""

# Example usage: Change status of issue with key "ABC-123" to "Done"
# change_issue_status("SKM-13")
