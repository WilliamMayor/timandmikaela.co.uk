import os
import urlparse
import datetime
from contextlib import contextmanager

import sh
from flask import current_app
from flask.ext.script import Manager, prompt
from flask.ext.migrate import MigrateCommand
from sqlalchemy import create_engine

import mim

manager = Manager(usage="Perform database operations")
manager.add_command('migrate', MigrateCommand)


def safe_to_print_url(url):
    parts = urlparse.urlparse(url)
    new_parts = list(parts)
    if parts.username is not None:
        new_parts[1] = new_parts[1].replace(parts.username, "******")
    if parts.password is not None:
        new_parts[1] = new_parts[1].replace(parts.password, "******")
    return urlparse.urlunparse(new_parts)


@contextmanager
def db_connect(url):
    engine = create_engine(url)
    conn = engine.connect()
    yield conn
    conn.close()


def ensure(name):
    try:
        os.makedirs(name)
    except OSError:
        pass


def get_db_url(url_or_name):
    if url_or_name is None:
        url_or_name = current_app.config['DATABASE_URL']
    elif url_or_name in os.environ:
        url_or_name = os.environ(url_or_name)
    return url_or_name


def replace_dbname(url, new_dbname):
    parts = urlparse.urlparse(url)
    new_parts = list(parts)
    new_parts[2] = '/%s' % new_dbname
    return urlparse.urlunparse(new_parts), parts[2][1:]


def parse_db_url(url):
    parts = urlparse.urlparse(url)
    return (
        parts.hostname, parts.port, parts.path.strip('/'),
        parts.username, parts.password)


@manager.option(
    '--url', '-u', dest='url',
    help='The DB to dump. Defaults to DATABASE_URL')
def dump(url=None):
    ensure('tmp')
    ensure('log')
    url = get_db_url(url)
    host, port, dbname, username, password = parse_db_url(url)
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    dump_file = '%s-%s.dump' % (dbname, date)
    local_path = 'tmp/%s' % dump_file
    args = [
        '--format=custom', '--file', local_path,
        '--host', host, '--port', port]
    if username:
        args += ['--username', username]
    env = os.environ.copy()
    if password:
        env['PGPASSWORD'] = password
    args.append(dbname)
    print 'Dumping DB to', local_path
    sh.pg_dump(*args, _env=env, _err='log/pg_dump_error.txt')
    return local_path


@manager.option(
    '--url', '-u', dest='url',
    help='The DB to restore into. Defaults to DATABASE_URL')
@manager.option(
    'dump_file',
    help='The file to load data from')
def restore(dump_file, url=None):
    ensure('log')
    url = get_db_url(url)
    host, port, dbname, username, password = parse_db_url(url)
    args = [
        '--verbose', '--clean', '--no-acl', '--no-owner',
        '--host', host, '--port', port, '--dbname', dbname]
    if username:
        args += ['--username', username]
    env = os.environ.copy()
    if password:
        env['PGPASSWORD'] = password
    args.append(dump_file)
    try:
        sh.pg_restore(*args, _env=env, _err='log/pg_restore_error.txt')
    except sh.ErrorReturnCode_1:
        print 'pg_restore exited with code 1'
        print 'this might be because of "harmless warnings"'
        print 'check the log: log/pg_restore_error.txt'


def confirm(url):
    host, port, dbname, user, password = parse_db_url(url)
    p = 'This will delete data, to confirm provide the name of the DB (%s)'
    check = prompt(p % dbname)
    assert check == dbname, '%s != %s, aborting' % (check, dbname)


@manager.option(
    '--url', '-u', dest='url',
    help='The DB to reset, defaults to DATABASE_URL')
def reset(url=None, heroku=False):
    """Drops and re-creates the database"""
    url = get_db_url(url)
    print 'Resetting:', safe_to_print_url(url)
    confirm(url)
    mim.models.db.drop_all()
    mim.models.db.create_all()


@manager.option(
    '--from', '-f', dest='_from',
    help='The name of the DB to pull data from. Defaults to DATABASE_URL')
@manager.option(
    '--to', '-t', dest='to',
    help='The URL for the local DB to push into. Defaults to DATABASE_URL')
def transfer(_from=None, to=None):
    """Move all data from one DB to another"""
    _from = get_db_url(_from)
    to = get_db_url(to)
    assert to != _from, 'Cannot transfer to and from the same DB'
    print 'From:', safe_to_print_url(_from)
    print 'To:', safe_to_print_url(to)
    confirm(to)
    local_path = dump(_from)
    restore(to, local_path)
