import json
import sys
import os
from datetime import datetime

TASKS_FILE = os.getenv(
    "TASKS_FILE", os.path.join(os.path.dirname(__file__), "..", "data", "tasks.json")
)


def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r", encoding="utf-8") as f:
        try:
            tasks = json.load(f)
        except json.JSONDecodeError:
            tasks = []
    return tasks


def save_tasks(tasks):
    os.makedirs(os.path.dirname(TASKS_FILE), exist_ok=True)
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=4, ensure_ascii=False)


def get_next_id(tasks):
    if tasks:
        return max(task["id"] for task in tasks) + 1
    else:
        return 1


def add_task(description):
    tasks = load_tasks()
    task_id = get_next_id(tasks)
    now = datetime.now().isoformat()
    task = {
        "id": task_id,
        "description": description,
        "status": "todo",
        "createdAt": now,
        "updatedAt": now,
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"Task added successfully (ID: {task_id})")


def update_task(task_id, new_description):
    tasks = load_tasks()
    found = False
    for task in tasks:
        if task["id"] == task_id:
            task["description"] = new_description
            task["updatedAt"] = datetime.now().isoformat()
            found = True
            break
    if found:
        save_tasks(tasks)
        print(f"Task {task_id} updated successfully.")
    else:
        print(f"Task with ID {task_id} not found.")


def delete_task(task_id):
    tasks = load_tasks()
    new_tasks = [task for task in tasks if task["id"] != task_id]
    if len(new_tasks) == len(tasks):
        print(f"Task with ID {task_id} not found.")
    else:
        save_tasks(new_tasks)
        print(f"Task {task_id} deleted successfully.")


def mark_task_status(task_id, new_status):
    tasks = load_tasks()
    valid_status = {"todo", "in-progress", "done"}
    if new_status not in valid_status:
        print(f"Invalid status: {new_status}")
        return
    found = False
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = new_status
            task["updatedAt"] = datetime.now().isoformat()
            found = True
            break
    if found:
        save_tasks(tasks)
        print(f"Task {task_id} marked as {new_status}.")
    else:
        print(f"Task with ID {task_id} not found.")


def list_tasks(filter_status=None):
    tasks = load_tasks()
    if filter_status:
        tasks = [task for task in tasks if task["status"] == filter_status]
    if not tasks:
        print("No tasks found.")
        return
    for task in tasks:
        print(
            f"ID: {task['id']} | Description: {task['description']} | Status: {task['status']} | Created: {task['createdAt']} | Updated: {task['updatedAt']}"
        )


def print_help():
    help_text = """
Usage:
    python task_tracker.py add "Task Description"
    python task_tracker.py update <id> "New Description"
    python task_tracker.py delete <id>
    python task_tracker.py mark-in-progress <id>
    python task_tracker.py mark-done <id>
    python task_tracker.py list [status]

Status can be: todo, in-progress, done
If no status is provided in the list command, all tasks will be displayed.
"""
    print(help_text)


def main():
    if len(sys.argv) < 2:
        print_help()
        sys.exit(1)

    command = sys.argv[1]
    if command == "add":
        if len(sys.argv) < 3:
            print("Please provide the task description.")
            sys.exit(1)
        description = sys.argv[2]
        add_task(description)
    elif command == "update":
        if len(sys.argv) < 4:
            print("Please provide the task ID and the new description.")
            sys.exit(1)
        try:
            task_id = int(sys.argv[2])
        except ValueError:
            print("Task ID must be an integer.")
            sys.exit(1)
        new_description = sys.argv[3]
        update_task(task_id, new_description)
    elif command == "delete":
        if len(sys.argv) < 3:
            print("Please provide the task ID.")
            sys.exit(1)
        try:
            task_id = int(sys.argv[2])
        except ValueError:
            print("Task ID must be an integer.")
            sys.exit(1)
        delete_task(task_id)
    elif command == "mark-in-progress":
        if len(sys.argv) < 3:
            print("Please provide the task ID.")
            sys.exit(1)
        try:
            task_id = int(sys.argv[2])
        except ValueError:
            print("Task ID must be an integer.")
            sys.exit(1)
        mark_task_status(task_id, "in-progress")
    elif command == "mark-done":
        if len(sys.argv) < 3:
            print("Please provide the task ID.")
            sys.exit(1)
        try:
            task_id = int(sys.argv[2])
        except ValueError:
            print("Task ID must be an integer.")
            sys.exit(1)
        mark_task_status(task_id, "done")
    elif command == "list":
        if len(sys.argv) == 2:
            list_tasks()
        else:
            filter_status = sys.argv[2]
            if filter_status not in ["todo", "in-progress", "done"]:
                print("Invalid status. Valid statuses are: todo, in-progress, done")
                sys.exit(1)
            list_tasks(filter_status)
    else:
        print("Unknown command.")
        print_help()


if __name__ == "__main__":
    main()
