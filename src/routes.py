from . import app
from flask import render_template, request, flash, g
from .models import History, db, Decision
import random
from sqlalchemy.exc import IntegrityError, DBAPIError
from werkzeug.utils import secure_filename
import os
from .auth import login_required


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

    if len(content_keys) > 1:
        decision = random.choice(values)
        if g.user:
            options = ', '.join(values)
            try:
                history = History(
                    options=options,
                    account_id=g.user.id
                )

                new_decision = Decision(
                    decision=decision,
                    account_id=g.user.id
                )
                db.session.add(history)
                db.session.add(new_decision)
                db.session.commit()

            except (DBAPIError, IntegrityError):
                flash('Something went wrong.')
                return render_template('home.html', decision=decision, values=values, content_keys=content_keys)
#                 return render_template('home.html', form=form, old_form=old_form)
        return render_template('home.html', decision=decision, values=values, content_keys=content_keys)

    return render_template('home.html', values=values, content_keys=content_keys)


def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/vision', methods=['POST', 'GET'])
@login_required
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


@app.route('/history')
def history():
    histories = History.query.filter_by(account_id=g.user.id).all()
    decisions = Decision.query.filter_by(account_id=g.user.id).all()
    return render_template('history.html', histories=histories, decisions=decisions)
