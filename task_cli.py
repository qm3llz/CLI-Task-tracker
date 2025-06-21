from pathlib import Path
import json
import sys
from datetime import datetime


tasks_file = Path("tasks.json")


if not tasks_file.exists():
    with tasks_file.open("w", encoding="utf-8") as f:
        json.dump([], f)


def load_tasks() -> list:
    if tasks_file.stat().st_size == 0:
        return []
    with tasks_file.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_tasks(tasks: list):
    with tasks_file.open("w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=4)


def generate_new_id(tasks):
    if not tasks:
        return 1
    return max(task["id"] for task in tasks) + 1


def add_task(description):
    tasks = load_tasks()
    new_id = generate_new_id(tasks)
    now = datetime.now().isoformat()
    new_task = {
        "id": new_id,
        "description": description,
        "status": "todo",
        "created": now,
        "updated": now,
    }
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Task added (id: {new_id})")


def update_task(task_id, new_description):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["description"] = new_description
            task["updated"] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task {task_id} updated")
            return
    print(f"Task {task_id} not found")


def delete_task(task_id):
    tasks = load_tasks()
    new_task = [task for task in tasks if task["id"] != task_id]
    if len(tasks) == len(new_task):
        print(f"Task {task_id} not found")
        return
    save_tasks(new_task)
    print(f"Task {task_id} deleted")


def mark_task(task_id, new_status):
    if new_status.lower() not in ["todo", "done", "in-progress"]:
        print("Invalid status. Use <task_tracker help>")
        return
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = new_status
            task["updated"] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task {task_id} marked as {new_status}")
            return
    print(f"Task {task_id} not found")


def list_tasks(filter_status=None):
    tasks = load_tasks()
    if filter_status:
        tasks = [task for task in tasks if task["status"] == filter_status]
    if not tasks:
        print("No task found")
        return
    for task in tasks:
        print(
            f"[{task['id']}] {task['description']} (Status: {task['status']}, Created: {task['created']}, updated: {task['updated']})"
        )


def usage():
    print('add "task description"')
    print('update <id> "new description"')
    print("delete <id>")
    print("mark-in-progress <id>")
    print("mark-done <id>")
    print("list [todo|in-progress|done]")


def main():
    if len(sys.argv) < 2:
        usage()
        return

    command = sys.argv[1]

    if command == "add":
        description = " ".join(sys.argv[2:]).strip()
        if not description:
            print("Enter a description")
            return
        add_task(description)

    elif command == "update":
        if len(sys.argv) < 4:
            print("Missing arguments for update.")
            usage()
            return
        try:
            task_id = int(sys.argv[2])
        except ValueError:
            print("Invalid task ID. It must be an integer.")
            return
        new_description = " ".join(sys.argv[3:]).strip()
        if not new_description:
            print("Enter a description")
            return
        update_task(task_id, new_description)

    elif command == "delete":
        if len(sys.argv) < 3:
            print("Missing task ID.")
            return
        try:
            task_id = int(sys.argv[2])
        except ValueError:
            print("Invalid task ID. It must be an integer.")
            return
        delete_task(task_id)

    elif command == "mark-in-progress":
        try:
            task_id = int(sys.argv[2])
        except ValueError:
            print("Invalid task ID. It must be an integer.")
            return
        mark_task(task_id, "in-progress")

    elif command == "mark-done":
        try:
            task_id = int(sys.argv[2])
        except ValueError:
            print("Invalid task ID. It must be an integer.")
            return
        mark_task(task_id, "done")

    elif command == "list":
        if len(sys.argv) == 3:
            status = sys.argv[2]
            if status not in ["todo", "in-progress", "done"]:
                print("Status must be one of: todo, in-progress, done")
                return
            list_tasks(status)
        else:
            list_tasks()

    elif command == "help":
        usage()

    else:
        print("Unknown command")
        usage()


if __name__ == "__main__":
    main()
