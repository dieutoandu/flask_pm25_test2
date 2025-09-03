from flask import Flask, render_template, Response
from datetime import datetime
from pm25 import get_mysql_data, write_data_to_mysql, get_avg_pm25, get_pm25_by_county
import json


books = {
    1: {
        "name": "Python book",
        "price": 299,
        "image_url": "https://im2.book.com.tw/image/getImage?i=https://www.books.com.tw/img/CN1/136/11/CN11361197.jpg&v=58096f9ck&w=348&h=348",
    },
    2: {
        "name": "Java book",
        "price": 399,
        "image_url": "https://im1.book.com.tw/image/getImage?i=https://www.books.com.tw/img/001/087/31/0010873110.jpg&v=5f7c475bk&w=348&h=348",
    },
    3: {
        "name": "C# book",
        "price": 499,
        "image_url": "https://im1.book.com.tw/image/getImage?i=https://www.books.com.tw/img/001/036/04/0010360466.jpg&v=62d695bak&w=348&h=348",
    },
}

app = Flask(__name__)


@app.route("/county_pm25/<county>")
def get_county_pm25(county):
    all_site = get_pm25_by_county(county)

    if len(all_site) == 0:
        return Response(json.dumps({"all_site": "can't not get data"}))
    site = [i[0] for i in all_site]
    pm25 = [float(i[1]) for i in all_site]
    data_time = all_site[0][2].strftime("%Y-%m-%d %H:%M:%S")
    return Response(
        json.dumps(
            {"all_site": len(site), "site": site, "pm25": pm25, "time": data_time},
            ensure_ascii=False,
        ),
        mimetype="application/json",
    )


@app.route("/avg_pm25")
def get_avg_pm25_():
    result = get_avg_pm25()
    county = [i[0] for i in result]
    pm25 = [float(i[1]) for i in result]

    return Response(
        json.dumps({"county": county, "pm25": pm25}, ensure_ascii=False),
        mimetype="application/json",
    )


@app.route("/update_db")
def update_data():
    datas = write_data_to_mysql()
    return f"datas : {datas}"


@app.route("/pm25")
def get_pm25():
    datas = get_mysql_data()
    countyEl = get_avg_pm25()
    county = [i[0] for i in countyEl]
    columns = ["site", "county", "pm25", "datacreationdate", "itemunit"]

    return render_template("pm25.html", content=datas, columns=columns, county=county)


@app.route("/bmi/height=<int:h>&weight=<int:w>")
def get_bmi(h, w):
    bmi = round(w / ((h / 100) ** 2), 2)
    return {"bmi": bmi}


@app.route("/books")
def get_book(id=None):

    return render_template("book.html", books=books)


@app.route("/nowtime")
def nowtime():
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return time


@app.route("/")
def index():
    time = nowtime()
    return render_template("index.html", time=time)


if __name__ == "__main__":
    app.run(debug=True)
