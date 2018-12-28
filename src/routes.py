from . import app
from flask import render_template, session
from .forms import ChoiceForm, ChoiceNumber
from wtforms import StringField
import random

@app.route('/', methods=['POST','GET'])
def home():
    """
    """
    choices = ChoiceNumber()
    form = ChoiceForm()

    if choices.validate_on_submit():
        number = choices.data['number']
        return render_template('home.html', number=number, form=form)

    if form.validate_on_submit():
        inputs = list(form.data.values())
        del inputs[-1]
        # removes csrf_token
        decision = random.choice(inputs)
        return render_template('home.html', decision=decision, form=form)

    return render_template('home.html', form=form)



