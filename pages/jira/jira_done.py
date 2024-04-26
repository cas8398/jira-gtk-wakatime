import requests
from requests.auth import HTTPBasicAuth
import json
from notifypy import Notify


def load_setting_data():
    with open("pages/jira/json/setting.json", "r") as file:
        data = json.load(file)
    return data


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

        # Read JSON data from file
        file_path = "pages/jira/json/jira_issues.json"
        with open(file_path, "r") as file:
            data = json.load(file)

        # Filter out the item with the specified ID
        filtered_data = [issue for issue in data if issue.get("id") != str(issue_key)]

        # Write the updated data back to the file
        with open(file_path, "w") as file:
            json.dump(filtered_data, file, indent=4)

        # Display desktop notification
        notification = Notify()
        notification.title = "Success !"
        notification.message = "issues: " + issue_title
        notification.icon = "assets/logo.png"
        notification.audio = "assets/notif.wav"
        notification.send()

    except requests.HTTPError as e:
        print(f"Failed to update issue status: {e}")

        # Display desktop notification
        notification = Notify()
        notification.title = "Error Description"
        notification.message = "status: : " + e
        notification.icon = "assets/logo.png"
        notification.audio = "assets/notif.wav"
        notification.send()


# Example usage: Change status of issue with key "ABC-123" to "Done"
# change_issue_status("SKM-13")
