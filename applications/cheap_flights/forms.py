from flask_wtf import FlaskForm
from wtforms import DateField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Optional

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

