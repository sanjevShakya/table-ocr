""" Main Flask App """
import os
import cv2
import time
from pytesseract import image_to_string
import util.preprocessing as preprocessing
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, make_response, redirect

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
            image = preprocessing.preprocess(image, rotate=int(rotate))
        else:
            image = preprocessing.rotate(image, rotate, scale=scale)
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
    else:
        return redirect("/")


@app.route("/extract", methods=["POST", "GET"])
def display_extract():
    if request.method == "POST" and request.form["image"]:
        file_location = request.form["image"]
        if file_location[-1] == "/":
            file_location = file_location[:-1]
        image = cv2.imread(file_location)
        # image = preprocessing.to_gray(image)
        return image_to_string(image)

    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
