from flask import Flask, render_template
from datetime import datetime


app = Flask(__name__)


@app.route("/")
def hello_world():
    current_year = datetime.now().year
    return render_template("main.html", year=current_year)


if __name__ == "__main__":
    app.run(debug=True)
