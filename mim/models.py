from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def init_app(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['DATABASE_URL']
    db.init_app(app)
    migrate.init_app(app, db)


class Accommodation(db.Model):
    aid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    type = db.Column(
        db.Enum(
            'bb', 'hotel', name='accommodation_type_enum'), nullable=False)
    distance = db.Column(db.Text, nullable=False)
    price = db.Column(db.Text, nullable=False)
    contact_name = db.Column(db.Text, nullable=False)
    contact_telephone = db.Column(db.Text)
    contact_mobile = db.Column(db.Text)
    contact_email = db.Column(db.Text)
    contact_address = db.Column(db.Text)
    contact_website = db.Column(db.Text)
    google_maps_url = db.Column(db.Text)

    @property
    def url_name(self):
        return self.name.lower().replace(' ', '')
