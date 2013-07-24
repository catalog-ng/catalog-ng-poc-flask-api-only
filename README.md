# CKAN 3.0 poc

[![Build Status](https://travis-ci.org/rshk/ckan3-poc-experiments.png?branch=master)](https://travis-ci.org/rshk/ckan3-poc-experiments)))]]

This is just a proof-of-concept of a possible way to make
[CKAN](http://ckan.org) way simpler, by making it do just one thing
in a nice & clean way.

**Author:** Samuele Santi <samuele.santi at trentorise dot eu>

**Date:** 2013-07-23

**License:** GNU Affero General Public License v3


## Basic concepts

* The "core" component of CKAN is the "data catalog".
* The data catalog is meant as a simple way to keep track of datasets
  available at a location.
* All the access to the catalog is done through a RESTful API.


## Technology

* Python -- the language of choice
* [Flask](http://flask.pocoo.org) -- the web framework
* [Flask-SQLAlchemy](http://pythonhosted.org/Flask-SQLAlchemy/)
  the ORM to access the database
* PostgreSQL 9.0+ -- to store catalog data (needs HSTORE)
* ElasticSearch -- to index catalog data for searches


## Data model

* ``package`` -- a "container", used to group resources
* ``resource`` -- a single data resource, usually referencing a URL

All the models are schemaless, that is, no structure is enforced,
but some fields have a special meaning.


## RESTful API

The API is greatly inspired by the [GitHub API](http://developer.github.com/v3/)
that I find very clean and well organized.


### Endpoints

All the API endpoints begin with ``/api/<n>/``, where ``<n>`` indicates the
API version (only ``1`` is supported at the moment).

* ``GET /package/`` - Packages listing / searching. Paginated (see below).
* ``POST /package/`` - Create a new package, taking attributes from the
  (json) request body
* ``GET /package/<id>/`` - Get a specific package
* ``PUT /package/<id>/`` - Update package attributes (override)
* ``PATCH /package/<id>/`` - Update package attributes (update)
* ``DELETE /package/<id>/`` - Delete package.
  **Note:** you must remove any associated reource before deleting a package!
* ``GET /package/<id>/resources/`` - Get resources from a package. Paginated.
* ``POST /package/<id>/resources/`` - Create a new resource associated
  with this package.
* ``GET /resource/`` - Resource listing/searching. Paginated.
* ``GET /resource/<id>/`` - Get a specific resource
* ``PUT /resource/<id>/`` - Update resource attributes (override)
* ``PATCH /resource/<id>/`` - Update resource attributes (update)
* ``DELETE /resource/<id>/`` - Delete resource


### Pagination

All the list/search endpoints support pagination.
The following GET arguments are supported in order to control pagination:

* ``page`` - Zero-based page number
* ``page_size`` - Amount of results per page to be returned

The ``Link`` header will contain links to first/prev/next/last pages.


## Testing

Preparation for test run:

* Create a fresh database (remember to CREATE EXTENSION hstore!)
* Copy local_settings.py -> local_settings_test.py and change settings

Running tests:

	CKAN_SETTINGS=$PWD/local_settings_test.py \
		py.test --pep8 -v ckan

Enable coverage report:

	CKAN_SETTINGS=$PWD/local_settings_test.py \
		py.test --pep8 -v ckan --cov=ckan --cov-report=term-missing
