import json
import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

PROJECT_NAME = "Student Study Planner"

DATA_FILE = os.path.join(app.root_path, "data", "tasks.json")

SUBJECTS = [
    "Python",
    "Mathematics",
    "Database (DBMS)",
    "Operating Systems",
    "Other"
]


def load_tasks():
    """Read all tasks from the JSON file and return them as a list."""
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_tasks(tasks):
    """Write the full list of tasks into the JSON file."""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=4)


def get_next_id(tasks):
    """Give every new task a number that is not used yet."""
    highest = 0

    for task in tasks:
        if task["id"] > highest:
            highest = task["id"]

    return highest + 1


def find_task(tasks, task_id):
    """Return the task with this id, or None if it does not exist."""
    for task in tasks:
        if task["id"] == task_id:
            return task

    return None


@app.route("/", methods=["GET", "POST"])
def home():
    error = None

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        subject = request.form.get("subject", "Other")
        due_date = request.form.get("due_date", "")

        if title == "":
            error = "Please type a task title before adding."

        else:
            tasks = load_tasks()

            new_task = {
                "id": get_next_id(tasks),
                "title": title,
                "subject": subject,
                "due_date": due_date,
                "done": False,
            }

            tasks.append(new_task)
            save_tasks(tasks)

            return redirect(url_for("home"))

    tasks = load_tasks()

    total = len(tasks)

    done_count = 0

    for task in tasks:
        if task["done"]:
            done_count += 1

    pending_count = total - done_count

    percent = 0

    if total > 0:
        percent = int(done_count * 100 / total)

    return render_template(
        "index.html",
        project_name=PROJECT_NAME,
        tasks=tasks,
        subjects=SUBJECTS,
        error=error,
        total=total,
        done_count=done_count,
        pending_count=pending_count,
        percent=percent,
    )


@app.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit(task_id):
    tasks = load_tasks()

    task = find_task(tasks, task_id)

    if task is None:
        return redirect(url_for("home"))

    error = None

    if request.method == "POST":
        title = request.form.get("title", "").strip()

        if title == "":
            error = "The task title cannot be empty."

        else:
            task["title"] = title
            task["subject"] = request.form.get("subject", "Other")
            task["due_date"] = request.form.get("due_date", "")

            save_tasks(tasks)

            return redirect(url_for("home"))

    return render_template(
        "edit.html",
        project_name=PROJECT_NAME,
        task=task,
        subjects=SUBJECTS,
        error=error,
    )


@app.route("/complete/<int:task_id>", methods=["POST"])
def complete(task_id):
    tasks = load_tasks()

    task = find_task(tasks, task_id)

    if task is not None:
        task["done"] = not task["done"]

    save_tasks(tasks)

    return redirect(url_for("home"))


@app.route("/delete/<int:task_id>", methods=["POST"])
def delete(task_id):
    tasks = load_tasks()

    remaining = []

    for task in tasks:
        if task["id"] != task_id:
            remaining.append(task)

    save_tasks(remaining)

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)