import requests
from flask import (
    Blueprint, render_template, redirect, url_for, abort, current_app)

from mim.models import db, Accommodation, BlogPost, GuestBookEntry
from mim.forms import RSVPForm, GuestBookForm

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
    return render_template('venue.html')


@public.route('/rsvp/', methods=['GET', 'POST'])
def rsvp():
    form = RSVPForm()
    if form.validate_on_submit():
        if form.email.data:
            requests.post(
                '%s/messages' % current_app.config['MAILGUN_URL'],
                auth=('api', current_app.config['MAILGUN_API_KEY']),
                data={
                    'from': 'Tim and Mikaela <thecouple@timandmikaela.co.uk>',
                    'to': form.email.data,
                    'subject': 'RSVP Confirmation',
                    'text': render_template(
                        'emails/rsvp_confirmation.txt', form=form)})
        requests.post(
            '%s/messages' % current_app.config['MAILGUN_URL'],
            auth=('api', current_app.config['MAILGUN_API_KEY']),
            data={
                'from': 'RSVP Bot <rsvpbot@timandmikaela.co.uk>',
                'to': 'thecouple@timandmikaela.co.uk',
                'subject': 'You Got an RSVP',
                'text': render_template(
                    'emails/rsvp_forward.txt', form=form)})
        return redirect(url_for('public.rsvp_thanks'))
    return render_template('rsvp.html', form=form)


@public.route('/rsvp/thanks/', methods=['GET'])
def rsvp_thanks():
    return render_template('rsvp_thanks.html')


@public.route('/giftlist/', methods=['GET'])
def giftlist():
    return render_template('giftlist.html')


@public.route('/blog/', methods=['GET'])
@public.route('/blog/<post>/', methods=['GET'])
def blog(post=None):
    posts = BlogPost.query.order_by(BlogPost.date).all()
    if post is None:
        return redirect(url_for('public.blog', post=posts[0].url_name))
    for p in posts:
        if p.url_name == post:
            break
    else:
        abort(404)
    return render_template('blog.html', post=p, posts=posts)


@public.route('/photos/', methods=['GET'])
@public.route('/photos/<album>/', methods=['GET'])
def photos(album=None):
    return 'OK'


@public.route('/guestbook/', methods=['GET'])
@public.route('/guestbook/<entry>/', methods=['GET'])
def guestbook(entry=None):
    entries = GuestBookEntry.query.order_by(GuestBookEntry.date).all()
    if entry is None:
        return redirect(
            url_for('public.guestbook', entry=entries[0].url_name))
    for e in entries:
        if e.url_name == entry:
            break
    else:
        abort(404)
    return render_template('guestbook_entry.html', entry=e, entries=entries)


@public.route('/guestbook/sign/', methods=['GET', 'POST'])
def guestbook_sign():
    form = GuestBookForm()
    if form.validate_on_submit():
        entry = GuestBookEntry()
        form.populate_obj(entry)
        db.session.add(entry)
        db.session.commit()
        requests.post(
            '%s/messages' % current_app.config['MAILGUN_URL'],
            auth=('api', current_app.config['MAILGUN_API_KEY']),
            data={
                'from': 'Tim and Mikaela <thecouple@timandmikaela.co.uk>',
                'to': form.email.data,
                'subject': 'Thanks for Signing Our Guest Book',
                'text': render_template(
                    'emails/guestbook_thanks.txt', entry=entry)})
        requests.post(
            '%s/messages' % current_app.config['MAILGUN_URL'],
            auth=('api', current_app.config['MAILGUN_API_KEY']),
            data={
                'from': 'Guest Book Bot <guestbookbot@timandmikaela.co.uk>',
                'to': 'thecouple@timandmikaela.co.uk',
                'subject': 'Someone Signed the Guest Book!',
                'text': render_template(
                    'emails/guestbook_forward.txt', entry=entry)})
        return redirect(
            url_for('public.guestbook', entry=entry.url_name))
    entries = GuestBookEntry.query.order_by(GuestBookEntry.date).all()
    return render_template('guestbook_sign.html', form=form, entries=entries)
