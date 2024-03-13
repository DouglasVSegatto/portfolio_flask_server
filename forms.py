from flask_wtf import FlaskForm
from wtforms import (DateField, FileField, IntegerField, PasswordField,
                     RadioField, SelectField, StringField, SubmitField)
from wtforms.validators import DataRequired, Email, NumberRange, Optional

""" Registration form """
#TODO - Add "Email" validation
class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[Email(), DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign Up")


""" Login form """

class LoginForm(FlaskForm):
    user_authentication = StringField("Username/Email", validators=[Email(), DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

airport_database = ["","YVR - Vancouver", "YYC - Calgary", "YEG - Edmonton", "YYZ - Toronto"]


class CheapFlights(FlaskForm):
    adults = IntegerField(label='Adults: *', validators=[DataRequired(), NumberRange(min=1, message="Please enter valid number")])
    fly_from = SelectField(label="Flight from: *", choices=airport_database, validators=[DataRequired()])
    fly_to = SelectField(label="Flight to: *", choices=airport_database, validators=[DataRequired()])
    date_from = DateField(label="Departure date range, from: *", validators=[DataRequired()])
    date_to = DateField(label="to: *", validators=[DataRequired()])
    return_from = DateField(label="Return date range, from:", validators=[Optional()])
    return_to = DateField(label="to:")
    nights_in_dst_from = IntegerField(label='Overnight stay duration, from:', validators=[NumberRange(min=1, message="Please enter valid number")])
    nights_in_dst_to = IntegerField(label='to:', validators=[NumberRange(min=1, message="Please enter valid number")])
    submit = SubmitField(label="Search")


class Img2Pdf(FlaskForm):
    conversion = RadioField(label='Choose your conversion',
                            choices=[('pdf_to_image', 'PDF to IMAGE'),
                                     ('image_to_pdf', 'IMAGE to PDF')],
                            validators=[DataRequired()])
    file = FileField(label="", validators=[DataRequired()])
    submit = SubmitField(label="Convert")