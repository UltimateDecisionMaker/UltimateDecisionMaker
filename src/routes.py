from . import app
from flask import render_template, session
from .forms import ChoiceForm
import random

@app.route('/', methods=['POST','GET'])
def home():
    """
    """
    form = ChoiceForm()

    # import pdb; pdb.set_trace()
    if form.validate_on_submit():
        choice1 = form.data['choice1']
        choice2 = form.data['choice2']
        decision = random.choice([choice1,choice2])
        return render_template('home.html', decision=decision, form=form)

    return render_template('home.html', form=form)

# @app.route('/webhooks/github', methods=['POST'])
# def github_post():
#     """
#     """
#     sender =  req.body.sender;
#     branch = req.body.ref;
