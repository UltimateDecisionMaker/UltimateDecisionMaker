from . import app
from .forms import AuthForm
from flask import render_template, session, flash, redirect, url_for, g
from .models import db, Account
import functools


# Decorator:
def login_required(view):
    """
    Here, view is a function. This decorator wrap up this function
    and require
    """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            # you can choose to redirect or abort
            # abort(404)
            flash("Please login first.")
            return redirect(url_for('.login'))

        # import pdb; pdb.set_trace()
        return view(**kwargs)

    # notice that we return uncalled wrapped_view function
    return wrapped_view


@app.before_request
def load_logged_in_user():
    """
    Go get the user id from session if exist
    """
    # import pdb; pdb.set_trace()
    # user_id = session.get('user_id')
    account_id = session.get('account_id')

    if account_id is None:
        g.user = None
    else:
        g.user = Account.query.get(account_id)


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

    return render_template('auth/register.html', form=form, error=error)

@app.before_request
def load_logged_in_account():
    account_id = session.get('account_id')

    if account_id is None:
        g.user = None
    else:
        g.user = Account.query.get(account_id)


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = AuthForm()

    error = None
    if form.validate_on_submit():
        email = form.data['email']
        password = form.data['password']

        account = Account.query.filter_by(email=email).first()

        if account is None or not account.check_password_hash(account, password):
            error = 'Invalid email or password'
        if error is None:
            session.clear()
            session['account_id'] = account.id

            flash("You were successfully logged in")
            return redirect(url_for(".home"))
    return render_template('auth/login.html', form=form, error=error)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    """
    """
    session.clear()
    flash('Logged out!')
    return redirect(url_for('.home'))
