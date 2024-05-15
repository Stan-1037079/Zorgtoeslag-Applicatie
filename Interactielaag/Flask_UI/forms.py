from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, IntegerField, SubmitField, FieldList, FormField, DateField
from wtforms.validators import DataRequired, InputRequired, Optional

class InputForm(FlaskForm):
    age_confirmation = BooleanField("Bent u 18 jaar of ouder?", validators=[Optional()])
    partner_confirmation = BooleanField("Heeft u een toeslagpartner?", validators=[Optional()])
    annual_income = IntegerField("Wat is uw jaarinkomen?", validators=[InputRequired()])
    assets = IntegerField("Wat is uw vermogen?", validators=[InputRequired()])
    submit = SubmitField("Verzenden")

class ChildForm(FlaskForm):
    date_of_birth = DateField("Wat is de geboortedatum van uw kind?", validators=[InputRequired()], format='%Y-%m-%d')

class InputFormkinderbijslag(FlaskForm):
    how_much_children = IntegerField("Hoeveel kinderen heeft u?", validators=[InputRequired()])
    children = FieldList(FormField(ChildForm), min_entries=1)
    submit = SubmitField("Verzenden")