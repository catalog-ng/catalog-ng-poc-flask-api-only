"""
Tests for the CKAN catalog API
"""

import json

import pytest

from ckan.catalog import db, app as ckan_app, Package


@pytest.fixture(scope="module")
def app(request):
    """Create a clean database, return test client"""

    db.drop_all()
    db.create_all()

    def fin():
        db.drop_all()
        request.addfinalizer(fin)

    return ckan_app.test_client()


def test_package_crud(app):
    result = app.get('/api/1/package/')
    assert result.status_code == 200

    ## To check that this is valid JSON
    data = json.loads(result.data)

    ## Make sure the db is empty
    assert len(data) == 0

    ## Create package
    obj = {
        'name': 'example-package',
        'title': 'Example Package',
        'license': 'cc-zero',
    }
    result = app.post('/api/1/package/',
                      data=json.dumps(obj),
                      content_type='application/json')
    assert result.status_code == 200
    new_obj = json.loads(result.data)
    for key in obj:
        assert new_obj[key] == obj[key]

    ## Check that the inserted object is ok
    dbobj = Package.query.filter_by(id=new_obj['id']).one()
    assert dbobj.attributes['name'] == obj['name']

    ## Check that we have it in the packages list
    result = app.get('/api/1/package/')
    assert result.status_code == 200
    data = json.loads(result.data)
    assert len(data) == 1
    assert new_obj['id'] == data[0]['id']

    ## Retrieve the package
    result = app.get('/api/1/package/{0}/'.format(new_obj['id']))
    assert result.status_code == 200
    data = json.loads(result.data)
    assert data['id'] == new_obj['id']
    for key in ('name', 'title', 'license'):
        assert data[key] == obj[key]
