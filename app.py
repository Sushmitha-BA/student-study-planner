from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)

SUBJECTS = [
    "Python",
    "Mathematics",
    "DBMS",
    "Operating Systems",
    "Other"
]

DATA_FILE = "data/tasks.json"


def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r") as file:
        return json.load(file)


def save_tasks(tasks):
    os.makedirs("data", exist_ok=True)

    with open(DATA_FILE, "w") as file:
        json.dump(tasks, file, indent=4)


@app.route("/", methods=["GET", "POST"])
def home():
    tasks = load_tasks()
    error = ""

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        subject = request.form.get("subject", "")
        due_date = request.form.get("due_date", "")

        if not title:
            error = "Task title cannot be empty."
        else:
            task = {
                "id": len(tasks) + 1,
                "title": title,
                "subject": subject,
                "due_date": due_date,
                "done": False
            }

            tasks.append(task)
            save_tasks(tasks)
            return redirect("/")

    return render_template(
        "index.html",
        project_name="Student Study Planner",
        tagline="Plan your subjects. Finish your tasks.",
        subjects=SUBJECTS,
        tasks=tasks,
        error=error
    )


if __name__ == "__main__":
    app.run(debug=True)