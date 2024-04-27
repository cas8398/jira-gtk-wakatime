import requests
from requests.auth import HTTPBasicAuth
import json
import shelve
import os
from gi.repository import Gtk
from .logging import log_message

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))


def load_setting_data():
    fix_path = os.path.join(current_dir, "json", "setting.json")
    with open(fix_path, "r") as file:
        data = json.load(file)
    return data


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

    # Extract the value corresponding to the "jira_url" key
    jira_url = next((item["jira_url"] for item in data if "jira_url" in item), None)
    jira_email = next((item["email"] for item in data if "email" in item), None)
    jira_token = next(
        (item["jira_token"] for item in data if "jira_token" in item), None
    )
    jira_id_done = next((item["id_done"] for item in data if "id_done" in item), None)

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
        dialog.connect("response", on_dialog_response)

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


def on_dialog_response(self, dialog, response_id):
    if response_id == Gtk.ResponseType.OK:
        # Call the reload_data function here
        print("reloaded.")


# Example usage: Change status of issue with key "ABC-123" to "Done"
# change_issue_status("SKM-13")
