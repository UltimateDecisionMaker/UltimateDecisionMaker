"""
In this file, we define all the inputs we gonna get and format them via FlaskForms.
"""

from flask import session
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, SelectField, PasswordField, IntegerField, TextAreaField
from wtforms.validators import DataRequired


class ChoiceForm(FlaskForm):
    choices = TextAreaField('choices')


class AuthForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
