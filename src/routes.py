from . import app
from flask import render_template, request, current_app
# from .forms import ChoiceForm, C_Form, CompanyForm, LocationForm
import random
import string

@app.route('/', methods=['POST', 'GET'])
# @app.cache.cached(timeout=300)  # cache this view for 5 minutes
def home():
    """
    """
    # grab data from user inputs in dynamic forms
    data = request.form
    keys = list(data.keys())
    values = list(data.values())

    # notice, to randomly select n out of m items:
    # random.shuffle(arr)
    # Take the first 2 elements of the now randomized array
    # print arr[0:2]

    # check if user has valid input
    if len(keys) > 1:
        # import pdb; pdb.set_trace()
        decision = random.choice(values)
        return render_template('home.html', decision=decision, values=values, string=string)
        # return render_template('home.html', decision=decision, form=form, old_form=old_form)

    # if old_form.validate_on_submit():
    #     choice1 = old_form.data['choice1']
    #     choice2 = old_form.data['choice2']
    #     decision = random.choice([choice1, choice2])
    #     return render_template('home.html', decision=decision, form=form, old_form=old_form)

    # return render_template("edit.html", form=form)

    # return render_template('home.html', form=form, old_form=old_form)
    return render_template('home.html', string=string)


# @app.route('/history/<user_id>', methods=['POST', 'GET'])
# def hisotry():
