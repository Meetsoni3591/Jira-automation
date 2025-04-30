import docx2txt
import json
import os

# Step 1: Extract text from .docx requirement document
def extract_text_from_docx(docx_path):
    return docx2txt.process(docx_path)

# Step 2: Parse tasks from text using simple keyword filtering
def parse_tasks_from_text(text):
    lines = text.split("\n")
    tasks = []
    for line in lines:
        if any(keyword in line.lower() for keyword in ["implement", "develop", "build", "create"]):
            tasks.append(line.strip())
    return tasks

# Step 3: Simulate Jira ticket creation (save to JSON)
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
        print(f"Simulated: {ticket_key} -> {task}")
    
    # Save to file
    with open(output_file, "w") as f:
        json.dump(simulated_tickets, f, indent=4)
    print(f"\nTickets saved to {output_file}")

if __name__ == "__main__":
    # Configurations
    docx_path = "requirement_docs/sample_project_requirements.docx"  # Use local docx
    output_file = "jira_tickets_simulated.json"

    # Run
    text = extract_text_from_docx(docx_path)
    tasks = parse_tasks_from_text(text)
    simulate_jira_ticket_creation(tasks, output_file)
