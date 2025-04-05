import os
import sys
import tempfile
import shutil
import subprocess
import unittest
import json


class TestTaskTrackerCLI(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.src_dir = os.path.join(self.test_dir, "src")
        self.data_dir = os.path.join(self.test_dir, "data")
        os.makedirs(self.src_dir, exist_ok=True)
        os.makedirs(self.data_dir, exist_ok=True)

        self.task_tracker_code = r'''
import json
import sys
import os
from datetime import datetime

TASKS_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "tasks.json")

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, 'r', encoding="utf-8") as f:
        try:
            tasks = json.load(f)
        except json.JSONDecodeError:
            tasks = []
    return tasks

def save_tasks(tasks):
    os.makedirs(os.path.dirname(TASKS_FILE), exist_ok=True)
    with open(TASKS_FILE, 'w', encoding="utf-8") as f:
        json.dump(tasks, f, indent=4, ensure_ascii=False)

def get_next_id(tasks):
    if tasks:
        return max(task['id'] for task in tasks) + 1
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
        "updatedAt": now
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"Tarefa adicionada com sucesso (ID: {task_id})")

def update_task(task_id, new_description):
    tasks = load_tasks()
    found = False
    for task in tasks:
        if task['id'] == task_id:
            task['description'] = new_description
            task['updatedAt'] = datetime.now().isoformat()
            found = True
            break
    if found:
        save_tasks(tasks)
        print(f"Tarefa {task_id} atualizada com sucesso.")
    else:
        print(f"Tarefa com ID {task_id} não encontrada.")

def delete_task(task_id):
    tasks = load_tasks()
    new_tasks = [task for task in tasks if task['id'] != task_id]
    if len(new_tasks) == len(tasks):
        print(f"Tarefa com ID {task_id} não encontrada.")
    else:
        save_tasks(new_tasks)
        print(f"Tarefa {task_id} deletada com sucesso.")

def mark_task_status(task_id, new_status):
    tasks = load_tasks()
    valid_status = {"todo", "in-progress", "done"}
    if new_status not in valid_status:
        print(f"Status inválido: {new_status}")
        return
    found = False
    for task in tasks:
        if task['id'] == task_id:
            task['status'] = new_status
            task['updatedAt'] = datetime.now().isoformat()
            found = True
            break
    if found:
        save_tasks(tasks)
        print(f"Tarefa {task_id} marcada como {new_status}.")
    else:
        print(f"Tarefa com ID {task_id} não encontrada.")

def list_tasks(filter_status=None):
    tasks = load_tasks()
    if filter_status:
        tasks = [task for task in tasks if task['status'] == filter_status]
    if not tasks:
        print("Nenhuma tarefa encontrada.")
        return
    for task in tasks:
        print(f"ID: {task['id']} | Descrição: {task['description']} | Status: {task['status']} | Criada: {task['createdAt']} | Atualizada: {task['updatedAt']}")

def print_help():
    help_text = """
Uso:
    python task_tracker.py add "Descrição da Tarefa"
    python task_tracker.py update <id> "Nova Descrição"
    python task_tracker.py delete <id>
    python task_tracker.py mark-in-progress <id>
    python task_tracker.py mark-done <id>
    python task_tracker.py list [status]

status pode ser: todo, in-progress, done
Se nenhum status for informado em list, todas as tarefas serão exibidas.
"""
    print(help_text)

def main():
    if len(sys.argv) < 2:
        print_help()
        sys.exit(1)

    command = sys.argv[1]
    if command == "add":
        if len(sys.argv) < 3:
            print("Por favor, informe a descrição da tarefa.")
            sys.exit(1)
        description = sys.argv[2]
        add_task(description)
    elif command == "update":
        if len(sys.argv) < 4:
            print("Por favor, informe o ID da tarefa e a nova descrição.")
            sys.exit(1)
        try:
            task_id = int(sys.argv[2])
        except ValueError:
            print("O ID da tarefa deve ser um número inteiro.")
            sys.exit(1)
        new_description = sys.argv[3]
        update_task(task_id, new_description)
    elif command == "delete":
        if len(sys.argv) < 3:
            print("Por favor, informe o ID da tarefa.")
            sys.exit(1)
        try:
            task_id = int(sys.argv[2])
        except ValueError:
            print("O ID da tarefa deve ser um número inteiro.")
            sys.exit(1)
        delete_task(task_id)
    elif command == "mark-in-progress":
        if len(sys.argv) < 3:
            print("Por favor, informe o ID da tarefa.")
            sys.exit(1)
        try:
            task_id = int(sys.argv[2])
        except ValueError:
            print("O ID da tarefa deve ser um número inteiro.")
            sys.exit(1)
        mark_task_status(task_id, "in-progress")
    elif command == "mark-done":
        if len(sys.argv) < 3:
            print("Por favor, informe o ID da tarefa.")
            sys.exit(1)
        try:
            task_id = int(sys.argv[2])
        except ValueError:
            print("O ID da tarefa deve ser um número inteiro.")
            sys.exit(1)
        mark_task_status(task_id, "done")
    elif command == "list":
        if len(sys.argv) == 2:
            list_tasks()
        else:
            filter_status = sys.argv[2]
            if filter_status not in ["todo", "in-progress", "done"]:
                print("Status inválido. Os status válidos são: todo, in-progress, done")
                sys.exit(1)
            list_tasks(filter_status)
    else:
        print("Comando desconhecido.")
        print_help()

if __name__ == "__main__":
    main()
'''
        self.task_tracker_path = os.path.join(self.src_dir, "task_tracker.py")
        with open(self.task_tracker_path, "w", encoding="utf-8") as f:
            f.write(self.task_tracker_code)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def run_command(self, args):

        cmd = [sys.executable, os.path.join("src", "task_tracker.py")] + args
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.test_dir)
        return result.stdout, result.stderr

    def test_add_task(self):
        stdout, _ = self.run_command(["add", "Comprar mantimentos"])
        self.assertIn("Tarefa adicionada com sucesso", stdout)
        tasks_file = os.path.join(self.test_dir, "data", "tasks.json")
        self.assertTrue(os.path.exists(tasks_file))
        with open(tasks_file, "r", encoding="utf-8") as f:
            tasks = json.load(f)
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["description"], "Comprar mantimentos")

    def test_update_task(self):
        self.run_command(["add", "Comprar mantimentos"])
        stdout, _ = self.run_command(
            ["update", "1", "Comprar mantimentos e preparar jantar"]
        )
        self.assertIn("Tarefa 1 atualizada com sucesso", stdout)
        tasks_file = os.path.join(self.test_dir, "data", "tasks.json")
        with open(tasks_file, "r", encoding="utf-8") as f:
            tasks = json.load(f)
        self.assertEqual(
            tasks[0]["description"], "Comprar mantimentos e preparar jantar"
        )

    def test_delete_task(self):
        self.run_command(["add", "Comprar mantimentos"])
        stdout, _ = self.run_command(["delete", "1"])
        self.assertIn("Tarefa 1 deletada com sucesso", stdout)
        tasks_file = os.path.join(self.test_dir, "data", "tasks.json")
        with open(tasks_file, "r", encoding="utf-8") as f:
            tasks = json.load(f)
        self.assertEqual(len(tasks), 0)

    def test_mark_in_progress(self):
        self.run_command(["add", "Comprar mantimentos"])
        stdout, _ = self.run_command(["mark-in-progress", "1"])
        self.assertIn("Tarefa 1 marcada como in-progress", stdout)
        tasks_file = os.path.join(self.test_dir, "data", "tasks.json")
        with open(tasks_file, "r", encoding="utf-8") as f:
            tasks = json.load(f)
        self.assertEqual(tasks[0]["status"], "in-progress")

    def test_mark_done(self):
        self.run_command(["add", "Comprar mantimentos"])
        stdout, _ = self.run_command(["mark-done", "1"])
        self.assertIn("Tarefa 1 marcada como done", stdout)
        tasks_file = os.path.join(self.test_dir, "data", "tasks.json")
        with open(tasks_file, "r", encoding="utf-8") as f:
            tasks = json.load(f)
        self.assertEqual(tasks[0]["status"], "done")

    def test_list_tasks(self):
        self.run_command(["add", "Task 1"])
        self.run_command(["add", "Task 2"])
        self.run_command(["mark-done", "2"])
        stdout_all, _ = self.run_command(["list"])
        self.assertIn("Task 1", stdout_all)
        self.assertIn("Task 2", stdout_all)
        stdout_todo, _ = self.run_command(["list", "todo"])
        self.assertIn("Task 1", stdout_todo)
        self.assertNotIn("Task 2", stdout_todo)
        stdout_done, _ = self.run_command(["list", "done"])
        self.assertIn("Task 2", stdout_done)
        self.assertNotIn("Task 1", stdout_done)


if __name__ == "__main__":
    unittest.main()
