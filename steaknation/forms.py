from flask_wtf import FlaskForm
from wtforms.fields import (
    StringField, DateField, TimeField, IntegerField, SubmitField,
    TextAreaField, PasswordField, EmailField)
from wtforms.validators import InputRequired, ValidationError, Email, EqualTo, DataRequired
from steaknation.models import User


class ReservationForm(FlaskForm):
    date = DateField("Date Of Reservation:", validators=[InputRequired()])
    time = TimeField("Time:", validators=[InputRequired()])
    num_of_people = IntegerField("Number Of People:", validators=[InputRequired()])
    comment = TextAreaField("Comment:")
    submit = SubmitField("Submit")


class LoginForm(FlaskForm):
    phone_number = StringField("Phone Number:", validators=[InputRequired()])
    password = PasswordField("Password:", validators=[InputRequired()])
    submit = SubmitField("Login")


class RegisterForm(FlaskForm):
    fullname = StringField("Name:", validators=[InputRequired()])
    phone_number = StringField("Phone Number:", validators=[InputRequired()])
    email = EmailField("Email", validators=[Email()], default="None@email.com")
    password = PasswordField("Password:", validators=[InputRequired()])
    confirm_password = PasswordField("Confirm Password:", validators=[InputRequired(), EqualTo('password'), DataRequired()])
    submit = SubmitField("Sign Up")

    def validate_phone_number(self, phone_number):
        if len(phone_number.data) < 10:
            raise ValidationError("Phone number entered is invalid. Please enter a valid phone number.")
        user = User.query.filter_by(phone_number=phone_number.data).first()
        if user:
            raise ValidationError("There is already an account registered by that phone number. Please choose another.")


class DeleteReservationForm(FlaskForm):
    submit = SubmitField("Delete")


class DeleteAccountForm(FlaskForm):
    submit = SubmitField("Delete")


class UpdateAccountForm(FlaskForm):
    change_email = EmailField("Change Email:")
    change_password = PasswordField("Change Password:")
    submit = SubmitField("Update")

