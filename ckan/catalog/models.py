from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import HSTORE
from sqlalchemy.ext.mutable import MutableDict

from .app import app


## Initialize database
db = SQLAlchemy(app)


## to query HSTORE:
## Package.query.filter(Package.attributes['example'] == 'hello').all()


# Catalog data can go in a configuration file
# http://www.w3.org/TR/vocab-dcat/#class-catalog


class Dataset(db.Model):
    ## See: http://www.w3.org/TR/vocab-dcat/#class-dataset
    id = db.Column(db.Integer, primary_key=True)
    attributes = db.Column(MutableDict.as_mutable(HSTORE))
    distributions = db.relationship(
        'Distribution',
        backref='package',
        lazy='dynamic')


class Distribution(db.Model):
    ## See: http://www.w3.org/TR/vocab-dcat/#class-distribution
    id = db.Column(db.Integer, primary_key=True)
    attributes = db.Column(MutableDict.as_mutable(HSTORE))
    dataset_id = db.Column(db.Integer, db.ForeignKey('dataset.id'))
