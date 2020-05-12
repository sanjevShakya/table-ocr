""" Main Flask App """
import os
import cv2
import sys
import csv
import time
import json
import numpy as np
from pytesseract import image_to_string
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, send_file, jsonify

sys.path.insert(0, os.path.abspath(".."))
from tableocr.util.table import get_cells
from tableocr.util.object import nested_list_to_json
import tableocr.util.image_preprocessing as preprocessing

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
IMAGE_FOLDER = os.path.join("static/images")
app.config["UPLOAD_FOLDER"] = IMAGE_FOLDER


@app.route("/", methods=["GET", "POST"])
def home():
    filename = None
    file_location = None
    if request.method == "POST":
        file = request.files["image"]

        if file.filename:
            filename = secure_filename(file.filename)
            file_location = os.path.join(basedir, app.config["UPLOAD_FOLDER"], filename)
            file.save(file_location)

            filename = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    return render_template("home.html", image=filename, file_location=file_location)


@app.route("/process", methods=["GET", "POST"])
def display_process():
    if request.method == "POST" and request.form["image"]:
        file_location = request.form["image"]
        if file_location[-1] == "/":
            file_location = file_location[:-1]
        rotate = int(request.form["rotate"]) if request.form["rotate"] else 0
        scale = float(request.form["scale"]) if request.form["scale"] else 1.0
        image = cv2.imread(file_location)
        if request.form.get("homograph"):
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            image = preprocessing.preprocess(image, rotate=int(rotate))
        else:
            image = preprocessing.rotate(image, rotate, scale=scale)
        
        kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        image = cv2.filter2D(image, -1, kernel)
        file_location = os.path.join(
            basedir, app.config["UPLOAD_FOLDER"], "temp", "1.png"
        )
        cv2.imwrite(file_location, image)

        # for directly displaying
        # _, buffer = cv2.imencode('.png', image)
        # response.headers['Content-Type'] = 'image/png'

        return render_template(
            "home.html",
            rotate=rotate,
            scale=scale,
            image=os.path.join(
                app.config["UPLOAD_FOLDER"],
                "temp",
                "1.png?now=" + str(time.strftime("%H%M%S", time.localtime())),
            ),
            file_location=file_location,
        )

    return redirect("/")


@app.route("/extract", methods=["POST", "GET"])
def display_extract():
    if request.method == "POST" and request.form["image"]:
        file_location = request.form["image"]
        if file_location[-1] == "/":
            file_location = file_location[:-1]
        image = cv2.imread(file_location)
        # image = preprocessing.to_gray(image)
        data = get_cells(image, int(request.form.get("column", 1)))
        if request.form.get("format") == "json" and data:
            data = nested_list_to_json(data[1:],data[0])
            with open("ocr-table-output.json", "w+") as file:
                json.dump(data, file, indent=2)

            return send_file('ocr-table-output.json',
                    mimetype='text/json',
                    attachment_filename='ocr-table-output.json',
                    as_attachment=True)

        elif request.form.get("format") == "csv" and data:

            with open('ocr-table-output.csv', "w+") as csv_file:
                csv_writer = csv.writer(csv_file, delimiter=",")
                csv_writer.writerow(data[0])
                for value in data[1:]:
                    csv_writer.writerow(value)

            return send_file('ocr-table-output.csv',
                    mimetype='text/json',
                    attachment_filename='ocr-table-output.csv',
                    as_attachment=True)
        else:
            return str(data)

    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
