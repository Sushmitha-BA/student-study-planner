from flask import Flask,render_template

app = Flask(__name__)

@app.route("/")
def home():
    project_name = "Student Study Planner"
    tagline = "Plan your subjects. Finish your tasks"
    return render_template ("index.html",project_name=project_name,tagline=tagline)
if __name__ == "__main__":
    app.run(debug=True)