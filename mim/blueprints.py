from flask import Blueprint, render_template, redirect, url_for, abort

from mim.models import Accommodation

public = Blueprint('public', __name__, template_folder='templates')


@public.route('/', methods=['GET'])
def home():
    return render_template('home.html')


@public.route('/accommodation/', methods=['GET'])
@public.route('/accommodation/<place>/', methods=['GET'])
def accommodation(place=None):
    all = Accommodation.query.order_by(Accommodation.name).all()
    if place is None:
        return redirect(url_for('public.accommodation', place=all[0].url_name))
    for a in all:
        if a.url_name == place:
            break
    else:
        abort(404)
    return render_template('accommodation.html', a=a, accommodation=all)


@public.route('/timetable/', methods=['GET'])
def timetable():
    return render_template('timetable.html')


@public.route('/venue/', methods=['GET'])
def venue():
    return 'OK'


@public.route('/rsvp/', methods=['GET', 'POST'])
def rsvp():
    return 'OK'


@public.route('/giftlist/', methods=['GET'])
def giftlist():
    return render_template('giftlist.html')


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
