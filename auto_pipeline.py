import os
# import ollama
import json
import docx2txt
from jira import JIRA
from github import Github
import openai
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# === ENV CONFIGURATION ===
DOCX_PATH = "requirement_docs/sample_project_requirements.docx"
JIRA_URL = os.getenv("JIRA_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
REPO_NAME = "Automation-testing"
TICKETS_JSON = "jira_tickets.json"
TEST_CASE_FOLDER = "test_cases"

# ========= STEP 1: Jira Ticket Automation ========= #

def extract_text(docx_path):
    return docx2txt.process(docx_path)

def parse_tasks(text):
    lines = text.split("\n")
    return [line.strip() for line in lines if any(k in line.lower() for k in ["build", "create", "implement", "design"])]

def create_jira_tickets(tasks):
    jira = JIRA(basic_auth=(JIRA_EMAIL, JIRA_TOKEN), options={"server": JIRA_URL})
    ticket_data = []
    for task in tasks:
        issue_dict = {
            'project': {'key': JIRA_PROJECT_KEY},
            'summary': task,
            'description': f"Auto-generated task: {task}",
            'issuetype': {'name': 'Task'},
        }
        issue = jira.create_issue(fields=issue_dict)
        ticket_data.append({'key': issue.key, 'summary': task})
        print(f"Created: {issue.key} -> {task}")
    with open(TICKETS_JSON, "w") as f:
        json.dump(ticket_data, f, indent=4)
    return ticket_data

# ========= STEP 2: GitHub Repo Automation ========= #

def create_repo_and_structure(ticket_data):
    g = Github(GITHUB_TOKEN)
    user = g.get_user()
    for repo in user.get_repos():
        if repo.name.lower() == REPO_NAME.lower():
            print(f"⚠️ Repository '{REPO_NAME}' already exists. Skipping creation.")
            return repo  # Return the existing repo object

    repo = user.create_repo(REPO_NAME)
    print(f"GitHub repo '{REPO_NAME}' created.")

     # Initial commit structure
    repo.create_file("README.md", "Initial commit", "# Auto Repo", branch="main")
    repo.create_file("src/.gitkeep", "Initial structure", "", branch="main")
    repo.create_file("tests/.gitkeep", "Initial structure", "", branch="main")
    
    main_branch = repo.get_branch("main")
    for ticket in ticket_data:
        branch = f"{ticket['key']}-{ticket['summary'].replace(' ', '-').lower()[:30]}"
        ref = f"refs/heads/{branch}"
        repo.create_git_ref(ref=ref, sha=main_branch.commit.sha)
        print(f"Created branch: {branch}")

#  STEP 3: Test Case Generation  #

def generate_test_cases(ticket):
    summary = ticket['summary']
    key = ticket['key']

    return f"""# Test Cases for {key} - {summary}

**Test Case 1**
- **ID**: TC-{key}-01
- **Description**: Verify the implementation of: {summary}
- **Steps**:
  1. Step 1: Setup necessary preconditions.
  2. Step 2: Perform action related to: {summary}
  3. Step 3: Validate the expected outcome.
- **Expected Result**: The system should successfully handle the scenario described in the summary.
- **Priority**: High

**Test Case 2**
- **ID**: TC-{key}-02
- **Description**: Validate edge cases and error handling for: {summary}
- **Steps**:
  1. Step 1: Input invalid/edge values.
  2. Step 2: Observe application behavior.
- **Expected Result**: The system should handle the edge case gracefully.
- **Priority**: Medium
"""

def save_test_cases(ticket, content):
    os.makedirs(TEST_CASE_FOLDER, exist_ok=True)
    file = os.path.join(TEST_CASE_FOLDER, f"{ticket['key']}_test_cases.md")
    with open(file, "w") as f:
        f.write(f"# Test Cases for {ticket['key']}: {ticket['summary']}\n\n")
        f.write(content)
    print(f"Saved test cases: {file}")



def run_pipeline():
    print("Extracting requirements...")
    text = extract_text(DOCX_PATH)

    print("Parsing tasks...")
    tasks = parse_tasks(text)

    print("Creating Jira tickets...")
    ticket_data = create_jira_tickets(tasks)

    print("Creating GitHub repository & branches...")
    create_repo_and_structure(ticket_data)

    print("Generating test cases...")
    for ticket in ticket_data:
        content = generate_test_cases(ticket)
        save_test_cases(ticket, content)

    print("\n✅ Automation Complete!")

if __name__ == "__main__":
    run_pipeline()
