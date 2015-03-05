import pprint
import os

from flask import current_app
from flask.ext.script import Manager, Server, prompt
from flask.ext.script.commands import Clean
from imgurpython import ImgurClient

from mim import create_app as mim_create_app
from mim.models import db, User

import database


def load_config(path):
    d = {}
    with open(path, 'rb') as fd:
        for line in fd.readlines():
            line = line.strip()
            if line:
                key, value = line.split('=', 1)
                d[key.upper().strip()] = value.strip()
    return d


def create_app(config=None):
    """Load data from config into ENV and create mim app"""
    env = {}
    try:
        env_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), '.env', 'default')
        env.update(load_config(env_path))
    except IOError:
        # e.g. running in Heroku
        print 'No default env file'
    if config is not None:
        env.update(load_config(config))
    os.environ.update(env)
    return mim_create_app()

manager = Manager(create_app)
manager.add_option(
    '-c', '--config', dest='config', required=False,
    help='Foreman-style env file that will be loaded into app\'s ENV')
manager.add_command('debug', Server(use_debugger=True))
manager.add_command('clean', Clean())
manager.add_command('database', database.manager)


@manager.command
def config():
    """Pretty prints the app's config"""
    pprint.pprint(dict(current_app.config))


@manager.command
def imgur_auth():
    """Run the initial Imgur auth flow"""
    client_id = current_app.config['IMGUR_CLIENT_ID']
    client_secret = current_app.config['IMGUR_CLIENT_SECRET']
    client = ImgurClient(client_id, client_secret)
    authorization_url = client.get_auth_url('token')
    print 'Please visit:', authorization_url
    access_token = prompt('Access Token')
    refresh_token = prompt('Refresh Token')
    client.set_user_auth(access_token, refresh_token)
    u = User.query.get(1)
    if u is None:
        u = User()
        u.uid = 1
    u.access_token = access_token
    u.refresh_token = refresh_token
    db.session.add(u)
    db.session.commit()


@manager.command
def envelope():
    """A place for performing one-off tasks.
    Define an envelope.py:run() method to use."""
    try:
        import envelope
        envelope.run()
    except ImportError:
        print 'No envelope module'

manager.run()
