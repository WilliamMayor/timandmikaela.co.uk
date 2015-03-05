from flask.ext.wtf import Form
from wtforms import TextField, RadioField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Optional, Email


class RSVPForm(Form):
    name = TextField(u'Your name...', validators=[DataRequired()])
    email = TextField(u'Your email...', validators=[Optional(), Email()])
    time = RadioField(
        choices=[
            (u'day', u'a day + evening guest'),
            (u'evening', u'an evening guest')])
    response = RadioField(
        choices=[
            (u'accept', u'would be delighted to accept'),
            (u'decline', u'must unfortunately decline')])
    starter = SelectField(choices=[
        (u'Sausage & Mash', u'Sausage & Mash'),
        (u'Prawn Cocktail', u'Prawn Cocktail'),
        (u'Leek & Potato Soup', u'Leek & Potato Soup')])


class GuestBookForm(Form):
    name = TextField(u'Name', validators=[DataRequired()])
    email = TextField(u'Email', validators=[DataRequired(), Email()])
    post = TextAreaField(u'Entry', validators=[DataRequired()])
