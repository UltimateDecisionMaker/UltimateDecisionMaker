from . import app
from flask import render_template
from .forms import ChoiceForm, C_Form, CompanyForm, LocationForm
import random


@app.route('/', methods=['POST', 'GET'])
def home():
    """
    """
    old_form = ChoiceForm()
    form = CompanyForm()

    # import pdb; pdb.set_trace()
    if old_form.validate_on_submit():
        choice1 = old_form.data['choice1']
        choice2 = old_form.data['choice2']
        decision = random.choice([choice1, choice2])
        return render_template('home.html', decision=decision, form=form, old_form=old_form)

    # return render_template("edit.html", form=form)
    return render_template('home.html', form=form, old_form=old_form)
