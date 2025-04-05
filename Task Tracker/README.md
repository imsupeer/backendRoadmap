Task Tracker
Build a CLI app to track your tasks and manage your to-do list.

Task Tracker is a project used to track and manage your tasks. In this task, you will build a simple Command Line Interface (CLI) to track what you need to do, what you have done, and what you are currently working on.

This project will help you practice your programming skills, including:

Working with the filesystem

Handling user inputs

Building a simple CLI application

✅ Requirements
The application should:

Run from the command line

Accept user actions and inputs as arguments

Store tasks in a JSON file

The user should be able to:
Add, update, and delete tasks

Mark a task as in progress or done

List all tasks

List tasks filtered by status:

Done

Not done (To Do)

In progress

⚙️ Constraints
You can use any programming language to build this project

Use positional arguments in the command line to accept user inputs

Use a JSON file to store the tasks in the current directory

The JSON file should be created if it does not exist

Use the native filesystem module of your programming language to interact with the JSON file

Do not use any external libraries or frameworks

Handle errors and edge cases gracefully

💻 Example Usage
bash
Copiar
Editar
# Adding a new task
task-cli add "Buy groceries"
# Output: Task added successfully (ID: 1)

# Updating and deleting tasks
task-cli update 1 "Buy groceries and cook dinner"
task-cli delete 1

# Marking a task as in progress or done
task-cli mark-in-progress 1
task-cli mark-done 1

# Listing all tasks
task-cli list

# Listing tasks by status
task-cli list done
task-cli list todo
task-cli list in-progress
📌 Task Properties
Each task should have the following properties:

id: A unique identifier for the task

description: A short description of the task

status: The status of the task (todo, in-progress, done)

createdAt: The date and time when the task was created

updatedAt: The date and time when the task was last updated

Make sure to add these properties to the JSON file when adding a new task, and update them when modifying a task.

🚀 Getting Started
1. Set Up Your Development Environment
Choose a programming language you are comfortable with (e.g., Python, JavaScript, etc.)

Ensure you have a code editor or IDE installed (e.g., VS Code, PyCharm)

2. Project Initialization
Create a new project directory for your Task Tracker CLI

Initialize version control (e.g., Git)

3. Implementing Features
Start by creating a basic CLI structure to handle user inputs

Implement features one by one, for example:

Add task

List tasks

Update tasks

Mark tasks

Delete tasks

4. Testing and Debugging
Test each feature individually to ensure they work as expected

Check the JSON file to verify that tasks are stored correctly

Debug issues as they arise

5. Finalizing the Project
Ensure all features are implemented and tested

Clean up your code and add comments where necessary

Write clear documentation (like this README) on how to use your Task Tracker CLI