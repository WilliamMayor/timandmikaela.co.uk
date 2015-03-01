import string


def filter_filter(_list, **kwargs):
    return filter(
        lambda li: all([getattr(li, k) == v for k, v in kwargs.iteritems()]),
        _list)


def init_app(app):
    app.jinja_env.filters['split'] = string.split
    app.jinja_env.filters['filter'] = filter_filter
    app.jinja_env.filters['just_date'] = lambda d: d.strftime('%Y-%m-%d')
