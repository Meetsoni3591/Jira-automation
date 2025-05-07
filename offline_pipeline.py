import docx2txt
import json
import os
from datetime import datetime

# ========== STEP 1: Extract & Parse Tasks ==========

def extract_text_from_docx(docx_path):
    return docx2txt.process(docx_path)

def parse_tasks_from_text(text):
    lines = text.split("\n")
    return [line.strip() for line in lines if any(k in line.lower() for k in ["implement", "develop", "build", "create"])]

# ========== STEP 2: Simulate Jira Ticket Creation ==========

def simulate_jira_ticket_creation(tasks, output_file="jira_tickets_simulated.json"):
    simulated_tickets = []
    for i, task in enumerate(tasks, start=1):
        ticket_key = f"SIM-{i}"
        ticket = {
            "key": ticket_key,
            "summary": task,
            "description": f"Simulated ticket for task: {task}"
        }
        simulated_tickets.append(ticket)
        print(f"✅ Jira Simulated: {ticket_key} -> {task}")
    
    with open(output_file, "w") as f:
        json.dump(simulated_tickets, f, indent=4)
    return simulated_tickets

# ========== STEP 3: Simulate GitHub Repo Setup ==========

def simulate_github_repo_setup(tickets, repo_name="simulated-project-repo"):
    os.makedirs(repo_name, exist_ok=True)
    with open(os.path.join(repo_name, "README.md"), "w") as f:
        f.write("# Simulated GitHub Repo\n\nCreated for testing the automation pipeline.")
    
    branches_dir = os.path.join(repo_name, "branches")
    os.makedirs(branches_dir, exist_ok=True)
    
    for ticket in tickets:
        branch_name = f"{ticket['key']}-{ticket['summary'].replace(' ', '-').lower()[:30]}"
        open(os.path.join(branches_dir, f"{branch_name}.txt"), "w").write(f"Simulated branch for: {ticket['summary']}")
        print(f"✅ GitHub Simulated Branch: {branch_name}")

# ========== STEP 4: Simulate AI-Based Test Case Generation ==========

def simulate_test_case_generation(ticket, output_dir="simulated_test_cases"):
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, f"{ticket['key']}_test_cases.md")
    
    fake_test_cases = f"""# Test Cases for {ticket['key']} - {ticket['summary']}

**Test Case 1**
- Description: Basic validation of "{ticket['summary']}"
- Steps: 
  1. Step one...
  2. Step two...
- Expected Result: Should function correctly
- Priority: High

**Test Case 2**
- Description: Edge case test
- Steps:
  1. Invalid input...
  2. Unexpected scenario...
- Expected Result: Should handle gracefully
- Priority: Medium
"""
    with open(file_path, "w") as f:
        f.write(fake_test_cases)
    
    print(f"✅ Test Cases Simulated: {file_path}")

# ========== MAIN PIPELINE ==========

def run_offline_pipeline():
    print("\n--- Starting Offline Automation Pipeline ---\n")
    
    text = extract_text_from_docx("requirement_docs/sample_project_requirements.docx")
    tasks = parse_tasks_from_text(text)
    
    tickets = simulate_jira_ticket_creation(tasks)
    simulate_github_repo_setup(tickets)
    
    for ticket in tickets:
        simulate_test_case_generation(ticket)
    
    print("\n🎉 Offline Simulation Complete!")

if __name__ == "__main__":
    run_offline_pipeline()
   