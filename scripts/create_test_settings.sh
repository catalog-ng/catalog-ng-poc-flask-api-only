#!/bin/bash

## Create local settings for CKAN3 testing

cat > local_settings_test.py <<EOF
# Ckan catalog settings for testing

SQLALCHEMY_DATABASE_URI = \
    "postgresql+psycopg2://postgresql@localhost/ckan3_test"

DEBUG = False

EOF
