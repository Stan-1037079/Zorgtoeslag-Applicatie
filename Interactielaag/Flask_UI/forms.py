from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, EmailField, SubmitField
from wtforms.validators import DataRequired, Email
import email_validator

class InputForm(FlaskForm):
    user_input = StringField('Enter name:', validators=[DataRequired()])
    description = TextAreaField('Enter surname:', validators=[DataRequired()])
    submit = SubmitField('Submit')
