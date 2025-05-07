import docx2txt
import json
import os
import re
from datetime import datetime

# Step 1: Extract text from .docx requirement document
def extract_text_from_docx(docx_path):
    if not os.path.exists(docx_path):
        raise FileNotFoundError(f"Document not found: {docx_path}")
    return docx2txt.process(docx_path)

# Step 2: Parse tasks from text using pattern matching
def parse_tasks_from_text(text):
    lines = text.split("\n")
    tasks = []
    current_main_task = None
    current_sub_tasks = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check for main task pattern [main-task]
        main_task_match = re.match(r'\[(.*?)\]', line)
        if main_task_match:
            # Save previous main task and its sub-tasks
            if current_main_task:
                tasks.append({
                    "main_task": current_main_task,
                    "sub_tasks": current_sub_tasks
                })
            # Start new main task without brackets
            current_main_task = main_task_match.group(1).strip()
            current_sub_tasks = []
        elif current_main_task and not line.startswith('['):
            current_sub_tasks.append(line)
    
    # Add the last main task and its sub-tasks
    if current_main_task:
        tasks.append({
            "main_task": current_main_task,
            "sub_tasks": current_sub_tasks
        })
    
    return tasks

# Step 3: Create Jira tickets with hierarchical structure
def create_jira_tickets(tasks, output_dir="."):
    tickets = []
    main_task_counter = 1

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_file = os.path.join(output_dir, f"jira_tickets_{timestamp}.json")

    for task_group in tasks:
        sub_task_counter = 1  # Reset per main task
        main_task_key = f"MAIN-{main_task_counter}"
        main_task = {
            "key": main_task_key,
            "summary": task_group["main_task"],
            "description": f"Main task: {task_group['main_task']}",
            "type": "Task",
            "sub_tasks": []
        }
        
        for sub_task in task_group["sub_tasks"]:
            sub_task_key = f"SUB-{main_task_counter}-{sub_task_counter}"
            sub_task_ticket = {
                "key": sub_task_key,
                "summary": sub_task,
                "description": f"Sub-task of {main_task_key}: {sub_task}",
                "type": "Sub-task",
                "parent": main_task_key
            }
            main_task["sub_tasks"].append(sub_task_ticket)
            sub_task_counter += 1
        
        tickets.append(main_task)
        main_task_counter += 1
    
    # Save to file
    with open(output_file, "w") as f:
        json.dump(tickets, f, indent=4)
    print(f"\nTickets saved to {output_file}")
    
    # Print summary
    print("\nCreated tickets:")
    for ticket in tickets:
        print(f"\n{ticket['key']}: {ticket['summary']}")
        for sub_task in ticket['sub_tasks']:
            print(f"  {sub_task['key']}: {sub_task['summary']}")

if __name__ == "__main__":
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Get the project root directory (one level up from script_dir)
    project_root = os.path.dirname(script_dir)
    
    # Paths
    docx_path = os.path.join(project_root, "requirement_docs", "labeled_project_requirements_for_jira.docx")
    output_dir = project_root  # Save to root with timestamped name

    try:
        text = extract_text_from_docx(docx_path)
        tasks = parse_tasks_from_text(text)
        create_jira_tickets(tasks, output_dir)
    except Exception as e:
        print(f"\nError: {e}")
