from . import app
from flask import render_template, request, flash, g
from .forms import ChoiceForm, C_Form, CompanyForm, LocationForm
from .models import History, db, Decision
import random
from sqlalchemy.exc import IntegrityError, DBAPIError


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
#         return render_template('home.html', decision=decision, form=form, old_form=old_form)


    # if old_form.validate_on_submit():
    #     choice1 = old_form.data['choice1']
    #     choice2 = old_form.data['choice2']
    #     decision = random.choice([choice1, choice2])
    #     return render_template('home.html', decision=decision, form=form, old_form=old_form)

    # return render_template("edit.html", form=form)


#     return render_template('home.html', form=form, old_form=old_form)
    return render_template('home.html', values=values, content_keys=content_keys)
    # return render_template('home.html')


@app.route('/history')
def history():
    histories = History.query.filter_by(account_id=g.user.id).all()
    decisions = Decision.query.filter_by(account_id=g.user.id).all()
    return render_template('history.html', histories=histories, decisions=decisions)
