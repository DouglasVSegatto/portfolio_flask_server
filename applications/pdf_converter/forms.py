from flask_wtf import FlaskForm
from wtforms import FileField, RadioField, SubmitField
from wtforms.validators import DataRequired


class Img2Pdf(FlaskForm):
    conversion = RadioField(label='Choose your conversion',
                            choices=[('pdf_to_image', 'PDF to IMAGE'),
                                     ('image_to_pdf', 'IMAGE to PDF')],
                            validators=[DataRequired()])
    file = FileField(label="", validators=[DataRequired()])
    submit = SubmitField(label="Convert")
