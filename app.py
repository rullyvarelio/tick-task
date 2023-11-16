from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todos.sqlite"

db = SQLAlchemy(app)

today = datetime.now()

today_day = today.strftime("%A")
today_date = today.strftime("%d")
today_month = today.strftime("%B")
today_year = today.strftime("%Y")

date_format = f"{today_day}, {today_date} {today_month} {today_year}"


class Todos(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    task = db.Column(db.String(100), nullable=False)
    datetime_created = db.Column(db.DateTime, default=today)
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
        print(request.form.getlist("is_task_content_done"))
        return redirect("/")


@app.route("/delete/<int:id>")
def delete(id):
    task_to_delete = Todos.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        return f"There was an issue adding your task: {e}"


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
