import requests
from requests.auth import HTTPBasicAuth
import json


def change_issue_status(issue_key):
    url = "https://cas8398.atlassian.net/rest/api/2/issue/" + issue_key + "/assignee"

    api_token = "ATATT3xFfGF0Ppa8IKI4B4gIW4bewnDOMZJtW0E_b0vq9AtqEl1Xnboquk9uH1idBp2TSoITzRdy4VvDO0kHiMbBgqZhZQ69mYrjxa_S1zroEKE_xYP1jZqVW9dePeLrr30ozGNDPLN5ZlJAN5UsxyDeC6d6LW7XrDNR4iwOaWJotIjcIjFLWx8=BFCDB504"

    auth = HTTPBasicAuth("cas8398@gmail.com", api_token)

    headers = {"Accept": "application/json", "Content-Type": "application/json"}

    # Payload to update the issue status to "Done"
    payload = json.dumps({"accountId": "5fc6af430dd553006fc8d508"})
    try:
        # Send PUT request to update the issue status
        response = requests.request(
            "PUT", url, data=payload, headers=headers, auth=auth
        )
        response.raise_for_status()  # Raise an exception for HTTP errors
        print("Issue status updated successfully.")
    except requests.HTTPError as e:
        print(f"Failed to update issue status: {e}")


# Example usage: Change status of issue with key "ABC-123" to "Done"
change_issue_status("SKM-13")
