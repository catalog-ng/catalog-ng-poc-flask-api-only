from flask import Flask

app = Flask(__name__)

## Configuration
app.config['DEBUG'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgresql+psycopg2://user:pass@pg.example.com/my-database'

app.config.from_envvar('CKAN_SETTINGS')
