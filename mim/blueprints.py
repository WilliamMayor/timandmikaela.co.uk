from flask import Blueprint, render_template

public = Blueprint('public', __name__, template_folder='templates')


@public.route('/', methods=['GET'])
def home():
    return render_template('base.html')


@public.route('/accommodation/', methods=['GET'])
@public.route('/accommodation/<place>/', methods=['GET'])
def accommodation(place=None):
    return 'OK'


@public.route('/timetable/', methods=['GET'])
def timetable():
    return 'OK'


@public.route('/venue/', methods=['GET'])
def venue():
    return 'OK'


@public.route('/rsvp/', methods=['GET', 'POST'])
def rsvp():
    return 'OK'


@public.route('/giftlist/', methods=['GET'])
def giftlist():
    return 'OK'


@public.route('/blog/', methods=['GET'])
@public.route('/blog/<post>/', methods=['GET'])
def blog(post=None):
    return 'OK'


@public.route('/photos/', methods=['GET'])
@public.route('/photos/<album>/', methods=['GET'])
def photos(album=None):
    return 'OK'


@public.route('/guestbook/', methods=['GET', 'POST'])
@public.route('/guestbook/<entry>/', methods=['GET'])
def guestbook(entry=None):
    return 'OK'
