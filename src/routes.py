from . import app
from flask import render_template, session
from .forms import ChoiceForm
from wtforms import StringField
import random

@app.route('/', methods=['POST','GET'])
def home():
    """
    """
    form = ChoiceForm()

    if form.validate_on_submit():
        inputs = form.data['choices'].split('\n')

        decision = random.choice(inputs)
        return render_template('home.html', decision=decision, form=form)

    return render_template('home.html', form=form)



