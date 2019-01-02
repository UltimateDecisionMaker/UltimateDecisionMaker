from . import app
from flask import render_template, request, flash, g
from .forms import ChoiceForm, C_Form, CompanyForm, LocationForm
from .models import History, db
import random
from sqlalchemy.exc import IntegrityError, DBAPIError


@app.route('/', methods=['POST', 'GET'])
def home():
    """
    """
    data = request.form
    keys = list(data.keys())
    values = list(data.values())

    old_form = ChoiceForm()
    form = CompanyForm()
    # import pdb; pdb.set_trace()

    # notice, to randomly select n out of m items:
    # random.shuffle(arr)
    # Take the first 2 elements of the now randomized array
    # print arr[0:2]
    if len(keys) > 1:
        if g.user:
            for val in values:
                try:
                    history = History(
                        options=val,
                        account_id=g.user.id
                    )
                    db.session.add(history)
                    db.session.commit()

                except (DBAPIError, IntegrityError):
                    flash('Something went wrong.')
                    return render_template('home.html', form=form, old_form=old_form)

        decision = random.choice(values)

        return render_template('home.html', decision=decision, form=form, old_form=old_form)

    # if old_form.validate_on_submit():
    #     choice1 = old_form.data['choice1']
    #     choice2 = old_form.data['choice2']
    #     decision = random.choice([choice1, choice2])
    #     return render_template('home.html', decision=decision, form=form, old_form=old_form)

    # return render_template("edit.html", form=form)

    return render_template('home.html', form=form, old_form=old_form)
    # return render_template('home.html')
