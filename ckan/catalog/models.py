from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import HSTORE
from sqlalchemy.ext.mutable import MutableDict

from .app import app


## Initialize database
db = SQLAlchemy(app)


## to query HSTORE:
## Package.query.filter(Package.attributes['example'] == 'hello').all()

class Package(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    attributes = db.Column(MutableDict.as_mutable(HSTORE))
    resources = db.relationship(
        'Resource',
        backref='package',
        lazy='dynamic')


class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    attributes = db.Column(MutableDict.as_mutable(HSTORE))
    package_id = db.Column(db.Integer, db.ForeignKey('package.id'))
