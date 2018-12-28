from . import app
from .forms import AuthForm
from flask import render_template, session, flash, redirect, url_for
from .models import db, Account


@app.route('/register', methods=['POST', 'GET'])
def register():
    """
    """

    form = AuthForm()

    error = None
    if form.validate_on_submit():
        email = form.data['email']
        password = form.data['password']

        if not email or not password:
            error = 'Invalid email or password'

        if Account.query.filter_by(email=email).first():
            error = f"{ email } has already been registered."

        if error is None:
            account = Account(email=email, password=password)
            db.session.add(account)
            db.session.commit()
            flash("Registration complete. Please Log in")
            return redirect(url_for('.login'))

        # flash(error)
    return render_template('auth/register.html', form=form, error=error)


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = AuthForm()

    error = None
    if form.validate_on_submit():
        email = form.data['email']
        password = form.data['password']
        # error = None

        account = Account.query.filter_by(email=email).first()

        if account is None or not account.check_password_hash(account, password):
            error = 'Invalid email or password'
        if error is None:
            session.clear()
            session['account_id'] = account.id

            flash("You were successfully logged in")
            return redirect(url_for(".home"))
    # error = "something wrong, can't proceed."
    return render_template('auth/login.html', form=form, error=error)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    """
    """
    session.clear()
    flash('Logged out!')
    return redirect(url_for('.login'))
