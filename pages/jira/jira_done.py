import requests
from requests.auth import HTTPBasicAuth
import json
from notifypy import Notify


def change_issue_done(issue_key, issue_title):
    url = "https://cas8398.atlassian.net/rest/api/2/issue/" + issue_key + "/transitions"

    api_token = "ATATT3xFfGF0Ppa8IKI4B4gIW4bewnDOMZJtW0E_b0vq9AtqEl1Xnboquk9uH1idBp2TSoITzRdy4VvDO0kHiMbBgqZhZQ69mYrjxa_S1zroEKE_xYP1jZqVW9dePeLrr30ozGNDPLN5ZlJAN5UsxyDeC6d6LW7XrDNR4iwOaWJotIjcIjFLWx8=BFCDB504"

    auth = HTTPBasicAuth("cas8398@gmail.com", api_token)

    headers = {"Accept": "application/json", "Content-Type": "application/json"}

    # Payload to update the issue status to "Done"
    payload = json.dumps({"transition": {"id": "31"}})
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
