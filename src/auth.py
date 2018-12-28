from . import app
from .forms import ChoiceForm, AuthForm
from flask import render_template, session, flash, redirect, url_for
from .models import db, Account


@app.route('/register', methods=['POST','GET'])
def register():
    form = AuthForm()

    if form.validate_on_submit():
        email = form.data['email']
        password = form.data['password']
        error = None

        if not email or not password:
            error = 'Invalid email or password'

        # if Account.query.filter_by(email=email).first
        # flash(error)
        if error is None:
            # flash("Registration complete")
            return redirect(url_for('.login'))

    return render_template('auth/register.html',form=form)


@app.route('/login', methods=['POST','GET'])
def login():
    form = AuthForm()

    if form.validate_on_submit():
        emial = form.data['email']
        password = form.data['password']
        error = None

        flash("OK..redirecting you to the home page...")
        # account = Account.query.filter_by(email=email).first()
        return redirect(url_for(".home"))
    error = "something wrong, can't proceed."
    flash(error)
    return render_template('auth/login.html', form=form)
