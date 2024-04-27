import requests
from requests.auth import HTTPBasicAuth
from gi.repository import Gtk
import json
import os
from .jira_done import change_issue_done
from .logging import log_message

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))


def load_setting_data():
    fix_path = os.path.join(current_dir, "json", "setting.json")
    with open(fix_path, "r") as file:
        data = json.load(file)
    return data


def change_issue_desc(issue_key, issue_title, update):
    # Load data from the file
    data = load_setting_data()

    # Extract the value corresponding to the "jira_url" key
    jira_url = next((item["jira_url"] for item in data if "jira_url" in item), None)
    jira_email = next((item["email"] for item in data if "email" in item), None)
    jira_token = next(
        (item["jira_token"] for item in data if "jira_token" in item), None
    )

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
