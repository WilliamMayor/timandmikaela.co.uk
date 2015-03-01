import pprint
import os

from flask import current_app
from flask.ext.script import Manager, Server
from flask.ext.script.commands import Clean

from mim import create_app as mim_create_app

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
def envelope():
    """A place for performing one-off tasks.
    Define an envelope.py:run() method to use."""
    try:
        import envelope
        envelope.run()
    except ImportError:
        print 'No envelope module'

manager.run()
