import os
import tensorflow as tf
import numpy as np

from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "animal_classificator/static/uploads"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
IMG_WIDTH = 256
IMG_HEIGHT = 256
labels = ['Cat', 'Dog']

model_path = 'animal_classificator/static/models//model_full.h5'

app = Flask(__name__, static_folder="static")
app.secret_key = "secret key"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def predict_class(image_path, model_path):
    model = tf.keras.models.load_model(model_path)

    img = tf.keras.utils.load_img(
        image_path, target_size=(IMG_WIDTH, IMG_HEIGHT))
    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)

    prediction_proba = model.predict(img_array)
    predicted_label = tf.where(prediction_proba < 0.5, 0, 1)
    label_proba = 100 * prediction_proba if prediction_proba > 0.5 else 100 * (1 - prediction_proba)

    label = predicted_label.numpy()[0][0]

    return labels[label], label_proba[0][0]


@app.route("/")
def upload_form():
    return render_template("index.html")


@app.route("/", methods=["POST"])
def upload_image():
    file = request.files["file"]
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        full_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(full_path)
        label, probability = predict_class(full_path, model_path)
        return render_template("index.html",
                                filename=filename,
                                label=label,
                                probability=probability)


def main():
   app.run(debug=False, host="0.0.0.0", port=9696)


if __name__ == "__main__":
    app.run()
