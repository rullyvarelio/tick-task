from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todos.sqlite"

db = SQLAlchemy(app)

today = datetime.now()
date_format = f"{today.strftime('%A')}, {today.strftime('%d')} {today.strftime('%B')} {today.strftime('%Y')}"


class Todos(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    task = db.Column(db.String(100), nullable=False)
    is_task_done = db.Column(db.Boolean, default=False)

    def __init__(self, task):
        self.task = task


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        task_content = request.form["task_content"]
        new_task = Todos(task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return f"There was an issue adding your task: {e}"
    else:
        tasks = Todos.query.order_by(Todos.id).all()
        return render_template("index.html", date_now=date_format, tasks=tasks)


@app.route("/check_task", methods=["POST", "GET"])
def check_task():
    if request.method == "POST":
        for task in Todos.query.all():
            checkbox_name = f"task_{task.id}"

            if checkbox_name in request.form:
                task.is_task_done = True
                db.session.commit()
    return redirect("/")


@app.route("/undo_task/<int:id>")
def undo(id):
    task_to_undo = Todos.query.get_or_404(id)

    try:
        task_to_undo.is_task_done = False
        db.session.commit()
        return redirect("/")
    except Exception as e:
        return f"There was an issue undoing your task: {e}"


@app.route("/edit_task/<int:id>", methods=["POST", "GET"])
def edit(id):
    task_to_update = Todos.query.get_or_404(id)
    if request.method == "POST":
        task_to_update.task = request.form["task_content"]

        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return f"There was an issue editing your task: {e}"
    return render_template("edit.html", task=task_to_update)


@app.route("/delete/<int:id>")
def delete(id):
    task_to_delete = Todos.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        return f"There was an issue deleting your task: {e}"


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
