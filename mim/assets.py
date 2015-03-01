from flask.ext.assets import Environment, Bundle

assets = Environment()

css = Bundle(
    'css/main.scss',
    filters='scss,cssmin',
    output='main.min.css',
    depends=['css/*.scss', 'css/base/*.scss'])
assets.register('css', css)

print_css = Bundle(
    'css/print.scss',
    filters='scss,cssmin',
    output='print.min.css',
    depends=['css/*.scss', 'css/base/*.scss'])
assets.register('print_css', print_css)

js = Bundle(
    'js/vendor/jquery-1.11.2.min.js',
    'js/vendor/jquery.slides.min.js',
    Bundle(
        'js/mim.js',
        'js/slides.js',
        'js/home.js',
        'js/venue.js',
        filters='rjsmin',
        depends='js/*.js'),
    output='main.min.js')
assets.register('js', js)


def init_app(app):
    assets.init_app(app)
