import os
import random
from . import app
from flask import render_template, request, flash, g
from .models import History, db, Decision
from sqlalchemy.exc import IntegrityError, DBAPIError
from werkzeug.utils import secure_filename
import os
from .auth import login_required



@app.route('/', methods=['POST', 'GET'])
def home():
    """
    """
    global values
    global decision
    global content_keys
    # grab data from user inputs in dynamic forms
    data = request.form
    content_keys = list(data.keys())[:-1]
    values = list(data.values())[:-1]

    # notice, to randomly select n out of m items:
    # random.shuffle(arr)
    # Take the first 2 elements of the now randomized array
    # print arr[0:2]

    if (request.method == 'POST') and (request.form["submit-button"] == "decide-for-me"):
        decision = random.choice(values)
        return render_template('home.html', decision=decision, values=values, content_keys=content_keys)
        # if g.user:
    if (g.user) and (request.method == 'POST') and (request.form["submit-button"] == "go-with-it"):
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
            flash("Success! Decision made and saved into your user history!")
            return render_template('home.html', decision=decision, values=values, content_keys=content_keys)

        except (DBAPIError, IntegrityError):
            flash('Something went wrong.')
            return render_template('home.html', decision=decision, values=values, content_keys=content_keys)
    return render_template('home.html', values=values, content_keys=content_keys)


def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/vision', methods=['POST', 'GET'])
@login_required
def vision():
    global img_name
    global choices
    global decision
    # initial upload
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

            response = client.text_detection(image=image)
            texts = response.text_annotations
            img_name = file.filename

            # reformat choices to make conditions compatible.
            choices = [_.description for _ in texts]

            return render_template('vision.html', img_name=img_name, choices=choices)

    # when user hit decide for me, or re-select.
    if (request.method == 'POST') and (request.form["submit-button"] == "decide-for-me"):
        data = request.form
        choices = list(data.values())[:-1]
        decision = random.choice(choices)
        return render_template('vision.html', img_name=img_name, choices=choices, decision=decision)

    # when user hit go-with-it, we push and save it to database.
    if (request.method == 'POST') and (request.form["submit-button"] == "go-with-it"):
        if g.user:
            options = ', '.join(choices)
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
                return render_template('vision.html', img_name=img_name, choices=choices)
        # hum...maybe we shall re direct user to some other place
        flash("Success! Decision made and saved into your user history!")
        return render_template('vision.html', img_name=img_name, choices=choices, decision=decision)
                # return render_template('home.html', decision=decision, values=values, content_keys=content_keys)
#                 return render_template('home.html', form=form, old_form=old_form)

    return render_template('vision.html')


@app.route('/history')
def history():
    histories = History.query.filter_by(account_id=g.user.id).all()
    decisions = Decision.query.filter_by(account_id=g.user.id).all()
    return render_template('history.html', histories=histories, decisions=decisions)
