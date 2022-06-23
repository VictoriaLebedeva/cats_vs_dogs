import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "animal_classificator/static/uploads"


app = Flask(__name__, static_folder="static")
app.secret_key = "secret key"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024


@app.route("/")
def upload_form():
    return render_template("index.html")


@app.route("/", methods=["POST"])
def upload_image():
    file = request.files["file"]
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        return render_template("index.html", filename=filename)


def main():
    app.run()


if __name__ == "__main__":
    app.run()
