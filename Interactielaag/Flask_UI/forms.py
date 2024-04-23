from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, IntegerField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Optional

class InputForm(FlaskForm):
    age_confirmation = BooleanField("Bent u 18 jaar of ouder?", validators=[Optional()])
    partner_confirmation = BooleanField("Hebt u een toeslagpartner?", validators=[Optional()])
    annual_income = IntegerField("Wat is uw jaarinkomen?", validators=[InputRequired()])
    assets = IntegerField("Wat is uw vermogen?", validators=[InputRequired()])
    submit = SubmitField("Verzenden")
