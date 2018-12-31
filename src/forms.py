"""
In this file, we define all the inputs we gonna get and format them via FlaskForms.
"""

from flask import session
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, SelectField, \
    PasswordField, FormField, FieldList, TextField
from wtforms.validators import DataRequired


class ChoiceForm(FlaskForm):
    choice1 = StringField('choice1', validators=[DataRequired()])
    choice2 = StringField('choice2', validators=[DataRequired()])


class AuthForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])


class C_Form(FlaskForm):
    choice = StringField('choice', validators=[DataRequired()])


class LocationForm(FlaskForm):
    location_id = StringField('location_id')
    city = StringField('city')


class CompanyForm(FlaskForm):
    company_name = StringField('company_name')
    locations = FieldList(FormField(LocationForm), min_entries=2)
