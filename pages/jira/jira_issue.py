import requests
from requests.auth import HTTPBasicAuth
import json
import os
from notifypy import Notify

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))


def load_setting_data():
    fix_path = os.path.join(current_dir, "json", "setting.json")
    with open(fix_path, "r") as file:
        data = json.load(file)
    return data


def update_issues():
    # Load data from the file
    data = load_setting_data()

    # Extract the value corresponding to the "jira_url" key
    jira_url = next((item["jira_url"] for item in data if "jira_url" in item), None)
    jira_email = next((item["email"] for item in data if "email" in item), None)
    jira_token = next(
        (item["jira_token"] for item in data if "jira_token" in item), None
    )

    # Start API
    url = f"https://{jira_url}/rest/api/3/search"
    auth = HTTPBasicAuth(jira_email, jira_token)
    headers = {"Accept": "application/json"}
    query = {"jql": 'status != "Done" ORDER BY created'}

    try:
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
            # Save the selected issues data to a JSON file
            fix_path_save = os.path.join(current_dir, "json", "jira_issues.json")
            output_file_path = fix_path_save

            # Delete the JSON file if it exists
            if os.path.exists(output_file_path):
                os.remove(output_file_path)

            with open(output_file_path, "w") as file:
                json.dump(selected_issues, file, indent=4)

            # Display desktop notification for success
            success_notification = Notify()
            success_notification.title = "Reload Issue Success"
            success_notification.message = "Issue list updated successfully"
            success_notification.icon = "assets/logo.png"
            success_notification.send()

        else:
            print("No issues found")  # Notify the user in case there are no issues
            # Display desktop notification for empty issue list
            empty_notification = Notify()
            empty_notification.title = "Reload Issue Warning"
            empty_notification.message = "Issues not found"
            empty_notification.icon = "assets/logo.png"
            empty_notification.send()

    except requests.RequestException as e:
        # Handle network errors or other request-related issues
        print("Error:", e)

        # Display desktop notification for failure
        error_notification = Notify()
        error_notification.title = "Reload Issue Fail"
        error_notification.message = f"Failed to update issue list: {str(e)}"
        error_notification.icon = "assets/logo.png"
        error_notification.send()
