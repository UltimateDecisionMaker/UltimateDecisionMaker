from . import app
from flask import render_template, request, flash
from werkzeug.utils import secure_filename
# from .forms import ChoiceForm, C_Form, CompanyForm, LocationForm
import random
import os
# import string


@app.route('/', methods=['POST', 'GET'])
# @app.cache.cached(timeout=300)  # cache this view for 5 minutes
def home():
    """
    """
    # grab data from user inputs in dynamic forms
    data = request.form
    content_keys = list(data.keys())
    values = list(data.values())

    # notice, to randomly select n out of m items:
    # random.shuffle(arr)
    # Take the first 2 elements of the now randomized array
    # print arr[0:2]

    # check if user has valid input
    if len(content_keys) > 1:
        # import pdb; pdb.set_trace()
        decision = random.choice(values)
        return render_template('home.html', decision=decision, values=values, content_keys=content_keys)

    return render_template('home.html', values=values, content_keys=content_keys)


def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/vision', methods=['POST', 'GET'])
def vision():
    global img_name
    if (request.method == 'POST') and (request.form["submit-button"] == "Upload"):
        if 'file' not in request.files:
            flash('No file part')
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(save_path)
            import io
            from google.cloud import vision
            from google.cloud.vision import types

            client = vision.ImageAnnotatorClient()

            with io.open(save_path, 'rb') as image_file:
                content = image_file.read()

            image = types.Image(content=content)

            # response = client.label_detection(image=image)
            # labels = response.label_annotations
            response = client.text_detection(image=image)
            texts = response.text_annotations

            # for label in labels:
            #     print(label.description)
            img_name = file.filename
            # return render_template('vision.html', img_name=file.filename, choices=labels)

            choices = [_.description for _ in texts]

            return render_template('vision.html', img_name=img_name, choices=choices)

    if (request.method == 'POST') and (request.form["submit-button"] == "decide-for-me"):
        # file = request.files['file']
        data = request.form
        choices = list(data.values())[:-1]
        decision = random.choice(choices)
        # import pdb; pdb.set_trace()
        # return render_template('vision.html', img_name=file.filename, choices=choices, decision=decision)
        return render_template('vision.html', img_name=img_name, choices=choices, decision=decision)


    return render_template('vision.html')
