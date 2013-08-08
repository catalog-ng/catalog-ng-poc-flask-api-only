"""
CKAN Catalog - the Core application, Flask-powered,
exposing RESTful access to the data catalog.
"""

from .models import db, Dataset, Distribution
from .api import api
from .app import app
