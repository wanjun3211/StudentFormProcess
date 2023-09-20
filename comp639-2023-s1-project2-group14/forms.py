# This is the registration form

# import libraries for forms
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, validators, RadioField
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired


def validate_email_domain(form, field):
    if not field.data.endswith('@lincolnuni.ac.nz'):
        raise validators.ValidationError(
            'Email must be from lincolnuni.ac.nz.')


# create a Signup form class with Flask Form
class SignUpForm(FlaskForm):
    first_name = StringField('First Name *', validators=[
                             DataRequired()], render_kw={"class": "form-control"})
    last_name = StringField('Last Name *', validators=[
                            DataRequired()], render_kw={"class": "form-control"})
    email = EmailField('Email *', validators=[DataRequired(), Email(), validate_email_domain], render_kw={
                       "class": "form-control"})
    password = PasswordField('Password *', validators=[
        DataRequired(), validators.Length(
            min=8, message='Password must be at least 8 characters long')
    ], render_kw={"class": "form-control"})
    confirm_password = PasswordField('Confirm Password *', validators=[DataRequired(), EqualTo(
        'password', message='Passwords must match!')], render_kw={"class": "form-control"})
    main_supervisor = StringField('Main Supervisor Full Name *', validators=[
        DataRequired()], render_kw={"class": "form-control"})
    submit = SubmitField('Sign Up', render_kw={"class": "btn btn-primary"})

    def validate_password(self, field):
        password = field.data
        has_upper = False
        has_digit = False
        has_special = False
        for char in password:
            if char.isupper():
                has_upper = True
            elif char.isdigit():
                has_digit = True
            elif char in '!@#$%^&*()_+-=[]{}|;:,.<>/?':
                has_special = True

        if not has_upper or not has_digit or not has_special:
            raise validators.ValidationError(
                'Password must contain at least one uppercase letter, one number, and one special character')


class SearchForm(FlaskForm):
    search_input = StringField('Search')
    submit_button = SubmitField('Search')
