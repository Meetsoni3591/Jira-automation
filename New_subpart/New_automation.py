import os
import json
import re
import docx2txt
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_URL = os.getenv("JIRA_URL")
JIRA_PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY")

auth = (JIRA_EMAIL, JIRA_API_TOKEN)
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

def extract_text_from_docx(docx_path):
    if not os.path.exists(docx_path):
        raise FileNotFoundError(f"Document not found: {docx_path}")
    return docx2txt.process(docx_path)

def parse_tasks_from_text(text):
    lines = text.split("\n")
    tasks = []
    current_main_task = []
    current_sub_tasks = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        main_task_match = re.match(r'\[.*?\]\s*(.*)', line)
        if main_task_match:
            if current_main_task:
                tasks.append({
                    "main_task": current_main_task,
                    "sub_tasks": current_sub_tasks
                })
            current_main_task = main_task_match.group(1).strip()
            current_sub_tasks = []
        elif current_main_task and not line.startswith('['):
            current_sub_tasks.append(line)

    if current_main_task:
        tasks.append({
            
            "main_task": current_main_task,
            "sub_tasks": current_sub_tasks
        }) 

    return tasks

def create_jira_issue(summary, description, issue_type="Task", parent_key=None):
    data = {
        "fields": {
            "project": {"key": JIRA_PROJECT_KEY},
            "summary": summary,
            "description": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": description
                            }
                        ]
                    }
                ]
            },
            "issuetype": {"id": "10035"}
        }
    }

    if issue_type.lower() == "task" and parent_key:
        data["fields"]["parent"] = {"key": parent_key}

    response = requests.post(f"{JIRA_URL}/rest/api/3/issue", headers=headers, auth=auth, json=data)

    if response.status_code == 201:
        issue_key = response.json()["key"]
        print(f"✅ Created {issue_type}: {issue_key} - {summary}")
        return issue_key
    else:
        print(f"\n❌ Failed to create {issue_type}: {summary}")
        print("Status Code:", response.status_code)
        print("Response:", response.text)
        return None


def create_jira_tickets(tasks):
    for main_index, task_group in enumerate(tasks, start=1):
        main_summary = task_group["main_task"]
        main_description = f"Main task: {main_summary}"
        main_issue_key = create_jira_issue(main_summary, main_description, "Task")

        if not main_issue_key:
            continue  # Skip sub-tasks 

        for sub_index, sub_task in enumerate(task_group["sub_tasks"], start=1):
            sub_summary = sub_task
            sub_description = f"Sub-task of {main_issue_key}: {sub_task}"
            create_jira_issue(sub_summary, sub_description, "Sub-task", parent_key=main_issue_key)

if __name__ == "__main__":
    # Resolve path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    docx_path = os.path.join(project_root, "requirement_docs", "labeled_project_requirements_for_jira.docx")

    try:
        text = extract_text_from_docx(docx_path)
        tasks = parse_tasks_from_text(text)
        create_jira_tickets(tasks)
    except Exception as e:
        print(f"\n❌ Error: {e}")
