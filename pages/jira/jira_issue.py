import os
import shelve
import requests
from requests.auth import HTTPBasicAuth
from gi.repository import Gtk
from .logging import log_message


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


def update_issues():
    try:
        # Load data from the file
        data = load_setting_data()

        # Extract the value corresponding to the "jira_url" key
        jira_url = data["jira_url"]
        jira_email = data["email"]
        jira_token = data["jira_token"]

        # Start API
        url = f"https://{jira_url}/rest/api/3/search"
        auth = HTTPBasicAuth(jira_email, jira_token)
        headers = {"Accept": "application/json"}
        query = {"jql": 'status != "Done" ORDER BY created'}

        log_message(log_level="info", menu_message="api issue", message=f"try load API")

        # Make a GET request to the Jira API
        response = requests.get(url, headers=headers, params=query, auth=auth)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes

        # Parse the JSON response
        data = response.json()

        # Initialize an empty list to store selected issues
        selected_issues = []

        # Iterate through each issue in the response data
        for issue in data["issues"]:
            # Check if the status of the issue is not "DONE"
            if issue["fields"]["status"]["statusCategory"]["key"] != "done":
                # Extract the title and issue ID from the current issue
                issue_title = issue["fields"]["summary"]
                project_name = issue["fields"]["project"]["name"]
                issue_id = issue["key"]

                # Create a dictionary containing the title and ID of the issue
                selected_issue = {
                    "project": project_name,
                    "id": issue_id,
                    "title": issue_title,
                }

                # Append the selected issue to the list
                selected_issues.append(selected_issue)

        if selected_issues:
            # Get the user's home directory
            home_dir = os.path.expanduser("~")

            # Initialize the shelve database file
            fix_path_save = os.path.join(home_dir, ".local", "share", "jira_issues_db")

            # Save the selected issues data to a shelve database
            with shelve.open(fix_path_save) as db:
                db["selected_issues"] = selected_issues

            log_message(
                log_level="info",
                menu_message="api issue",
                message=f"issue success loaded",
            )
            # Show error message
            dialog = Gtk.MessageDialog(
                flags=0,
                message_type=Gtk.MessageType.OTHER,
                buttons=Gtk.ButtonsType.OK,
                text="info \n issue success loaded",
            )
            dialog.run()
            dialog.destroy()

        else:
            log_message(
                log_level="warning",
                menu_message="api issue",
                message=f"issue list found",
            )
            # Show error message
            dialog = Gtk.MessageDialog(
                flags=0,
                message_type=Gtk.MessageType.OTHER,
                buttons=Gtk.ButtonsType.OK,
                text="warning \n issue list null",
            )
            dialog.run()
            dialog.destroy()

    except requests.RequestException as e:
        # Handle network errors or other request-related issues
        error_message = f"Error loading issues from API: {e}"
        print(error_message)
        log_message(log_level="error", menu_message="api issue", message=error_message)
        # Show error message
        dialog = Gtk.MessageDialog(
            flags=0,
            message_type=Gtk.MessageType.OTHER,
            buttons=Gtk.ButtonsType.OK,
            text="Error \n loading issues from API",
        )
        dialog.run()
        dialog.destroy()
