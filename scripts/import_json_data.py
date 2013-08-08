#!/usr/bin/env python

## Import data from CKAN json file

from ckan.catalog import db, Dataset, Distribution
import json

## todo: ``CREATE EXTENSION hstore`` too?
db.create_all()

data = json.load(open('/tmp/ckandb.json', 'r'))

def row_to_hstore(row):
    hstorable = {}
    for key, val in row.iteritems():
        if isinstance(val, (list, tuple)):
            val = ", ".join(val)

        elif isinstance(val, (int, float)):
            val = str(val)

        elif isinstance(val, basestring):
            pass

        else:
            val = json.dumps(val)
            
        #val = json.dumps(val)
        hstorable[key] = val
    return hstorable

for row_id, row in enumerate(data):
    print "Row:", row_id
    
    _row = row.copy()
    del _row['resources']

    pkg = Dataset()
    pkg.attributes = row_to_hstore(_row)
    db.session.add(pkg)

    for resource in row['resources']:
        res = Distribution()
        res.attributes = row_to_hstore(resource)
        res.dataset = pkg
        db.session.add(res)

    db.session.commit()

