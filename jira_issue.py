# This code sample uses the 'requests' library:
# http://docs.python-requests.org
import requests
from requests.auth import HTTPBasicAuth
import json

url = "https://cas8398.atlassian.net/rest/api/3/search"

api_token = "ATATT3xFfGF0Ppa8IKI4B4gIW4bewnDOMZJtW0E_b0vq9AtqEl1Xnboquk9uH1idBp2TSoITzRdy4VvDO0kHiMbBgqZhZQ69mYrjxa_S1zroEKE_xYP1jZqVW9dePeLrr30ozGNDPLN5ZlJAN5UsxyDeC6d6LW7XrDNR4iwOaWJotIjcIjFLWx8=BFCDB504"


auth = HTTPBasicAuth("cas8398@gmail.com", api_token)

headers = {"Accept": "application/json"}

query = {"jql": 'status != "Done" ORDER BY created'}

response = requests.request("GET", url, headers=headers, params=query, auth=auth)

# Parse the JSON response
data = response.json()


# Initialize an empty list to store selected issues
selectedIssues = []

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
        selectedIssues.append(selected_issue)

# Save the selected issues data to a JSON file
output_file_path = "jira_issues.json"
with open(output_file_path, "w") as f:
    json.dump(selectedIssues, f, indent=4)
