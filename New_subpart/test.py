import os
import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

# Load .env credentials
load_dotenv()
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_URL = os.getenv("JIRA_URL")
PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY")

# Auth
auth = HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)

# Headers
headers = {
    "Accept": "application/json"
}

# Endpoint to get issue types available for the project
url = f"{JIRA_URL}/rest/api/3/issuetype/project?projectIdOrKey={PROJECT_KEY}"

response = requests.get(url, headers=headers, auth=auth)

if response.status_code == 200:
    issue_types = response.json()["issueTypes"]
    print(f"\n✅ Available issue types in project '{PROJECT_KEY}':\n")
    for itype in issue_types:
        print(f"- {itype['name']} (ID: {itype['id']})")
else:
    print(f"\n❌ Failed to fetch issue types")
    print(f"Status Code: {response.status_code}")
    print("Response:", response.text)
