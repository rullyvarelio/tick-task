from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todos.db"

db = SQLAlchemy(app)

today = datetime.now()

today_day = today.strftime("%A")
today_date = today.strftime("%d")
today_month = today.strftime("%B")
today_year = today.strftime("%Y")

date_format = f"{today_day}, {today_date} {today_month} {today_year}"


class Todos(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    content = db.Column("content", db.String(100), nullable=False)
    date_created = db.Column("date_created", db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<Task %r>" % self.id

    # def __init__(self, content, date_created):
    #     self.content = content
    #     self.date_created = date_created


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        task_content = request.form["content"]
        new_task = Todos(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return f"There was an issue adding your task: {e}"
    else:
        tasks = Todos.query.order_by(Todos.date_created).all()
        return render_template("index.html", date_now=date_format, tasks=tasks)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
