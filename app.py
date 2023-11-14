from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)

today = datetime.now()

today_day = today.strftime("%A")
today_date = today.strftime("%d")
today_month = today.strftime("%B")
today_year = today.strftime("%Y")

date_format = f"{today_day}, {today_date} {today_month} {today_year}"


@app.route("/", methods=["POST", "GET"])
def index():
    return render_template("index.html", date_now=date_format)


if __name__ == "__main__":
    app.run(debug=True)
