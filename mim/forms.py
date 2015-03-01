from flask.ext.wtf import Form
from wtforms import TextField, RadioField, SelectField
from wtforms.validators import DataRequired, Optional, Email


class RSVPForm(Form):
    name = TextField(u'Your name...', validators=[DataRequired()])
    email = TextField(u'Your email...', validators=[Optional(), Email()])
    response = RadioField(
        default='accept',
        choices=[
            (u'accept', u'I would be delighted to accept'),
            (u'decline', u'I must unfortunately decline')])
    starter = SelectField(choices=[
        (u'Sausage & Mash', u'Sausage & Mash'),
        (u'Prawn Cocktail', u'Prawn Cocktail'),
        (u'Leek & Potato Soup', u'Leek & Potato Soup')])
