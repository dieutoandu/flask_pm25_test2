from flask import Flask
from datetime import datetime

app = Flask(__name__)


@app.route("/bmi/height=<int:h>&weight=<int:w>")
def get_bmi(h, w):
    bmi = round(w / ((h / 100) ** 2), 2)
    return {"bmi": bmi}


@app.route("/books")
@app.route("/books/id=<int:id>")
def get_book(id=None):
    try:
        books = {1: "Python book", 2: "Java book", 3: "Flask book"}

        if id == None:
            return books

        return books[id]

    except Exception as e:
        return f"erro + : {e}"


@app.route("/nowtime")
def nowtime():
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return time


@app.route("/")
def index():
    return "hello Flask my name is irving !"


if __name__ == "__main__":
    app.run(debug=True)
