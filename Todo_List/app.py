from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

tasks = [
    {"content": "Finish project", "done": False, "priority": True, "due_date": "2025-04-25T18:00", "id": 0},
    {"content": "Read a book", "done": False, "priority": False, "due_date": "", "id": 1}
]

@app.route("/")
def index():
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add_task():
    task_content = request.form["task"]
    due_date = request.form.get("due_date", "")
    priority = "priority" in request.form
    task_id = len(tasks)

    tasks.append({
        "content": task_content,
        "done": False,
        "priority": priority,
        "due_date": due_date,
        "id": task_id
    })

    return redirect(url_for("index"))

@app.route("/toggle/<int:task_id>")
def toggle_task(task_id):
    task = tasks[task_id]
    task["done"] = not task["done"]
    return redirect(url_for("index"))

@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    tasks.pop(task_id)
    return redirect(url_for("index"))

@app.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    task = tasks[task_id]
    if request.method == "POST":
        task["content"] = request.form["task"]
        task["due_date"] = request.form.get("due_date", "")
        task["priority"] = "priority" in request.form
        return redirect(url_for("index"))
    return render_template("edit_task.html", task=task)

if __name__ == "__main__":
    app.run(debug=True)
