import requests
from requests.auth import HTTPBasicAuth
import json
from notifypy import Notify
from pages.jira.jira_desc import change_issue_desc


def load_setting_data():
    with open("pages/jira/json/setting.json", "r") as file:
        data = json.load(file)
    return data


def change_assign_status(issue_key, issue_title, timeData):
    # Load data from the file
    data = load_setting_data()

    # Extract the value corresponding to the "jira_url" key
    jira_url = next((item["jira_url"] for item in data if "jira_url" in item), None)
    jira_email = next((item["email"] for item in data if "email" in item), None)
    jira_token = next(
        (item["jira_token"] for item in data if "jira_token" in item), None
    )
    jira_accountId = next(
        (item["accountId"] for item in data if "accountId" in item), None
    )
    jira_desc = (
        next((item["default_desc"] for item in data if "default_desc" in item), None)
        if timeData == ""
        else str(timeData)
    )
    print("default_desc:", jira_desc)

    # Start API
    url = f"https://{jira_url}/rest/api/2/issue/{issue_key}/assignee"

    auth = HTTPBasicAuth(jira_email, jira_token)

    headers = {"Accept": "application/json", "Content-Type": "application/json"}

    # Payload to update the issue status to "Done"
    payload = json.dumps({"accountId": jira_accountId})
    try:
        # Send PUT request to update the issue status
        response = requests.request(
            "PUT", url, data=payload, headers=headers, auth=auth
        )
        response.raise_for_status()  # Raise an exception for HTTP errors
        print("Issue status updated successfully.")

        # run change desc
        change_issue_desc(issue_key, issue_title, jira_desc)

    except requests.HTTPError as e:
        print(f"Failed to update issue status: {e}")

        # Display desktop notification
        notification = Notify()
        notification.title = "Error Assigned"
        notification.message = "status: : " + str(e)
        notification.icon = "assets/logo.png"
        notification.audio = "assets/notif.wav"
        notification.send()


# Example usage: Change status of issue with key "ABC-123" to "Done"
# change_issue_status("SKM-13")
