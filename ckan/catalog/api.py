import urllib
from math import ceil

from flask import request
from flask.ext import restful
from sqlalchemy.orm.exc import NoResultFound

from .app import app
from .models import db, Package, Resource


api = restful.Api(app)


class ModelResource(restful.Resource):
    """
    Common methods for exposing SQLAlchemy models through
    flask-restful
    """

    model = None  # Must be overridden by subclasses
    _query = None

    @property
    def query(self):
        if self._query is not None:
            return self._query
        return self.model.query

    def _serialize(self, obj):
        data = {}
        if obj.attributes is not None:
            data.update(obj.attributes)
        data['id'] = obj.id
        return data

    def _get(self, obj_id):
        try:
            return self.query.filter_by(id=obj_id).one()
        except NoResultFound:
            restful.abort(404, message='Requested object not found')

    def get(self, obj_id=None):
        if obj_id is None:
            ## todo: load filters from arguments
            query = self.query

            ## Pagination
            page_size = 10
            page = 0
            if 'page_size' in request.args:
                try:
                    page_size = int(request.args['page_size'])
                except ValueError:
                    restful.abort(400, message="Page size must be an integer")
                if page_size < 1:
                    restful.abort(
                        400, message="Page size must be greater than zero")
                if page_size > 100:
                    page_size = 100

            pages_count = int(ceil(query.count() * 1.0 / page_size))
            max_page = pages_count - 1

            if 'page' in request.args:
                page = int(request.args['page'])
                if page < 0:
                    restful.abort(
                        400, message='Page number cannot be negative')
                if page > max_page:
                    restful.abort(404, message='Page number out of range')

            ## Pagination links
            links = []

            def get_url(**kw):
                args = dict(request.args)
                args.update(kw)
                query_string = urllib.urlencode(args)
                if query_string:
                    return '{0}?{1}'.format(request.base_url, query_string)
                return request.base_url

            if page > 0:
                links.append("<{0}>; rel=\"first\""
                             "".format(get_url(page=0,
                                               page_size=page_size)))
                links.append("<{0}>; rel=\"prev\""
                             "".format(get_url(page=page-1,
                                               page_size=page_size)))
            if page < max_page:
                links.append("<{0}>; rel=\"next\""
                             "".format(get_url(page=page+1,
                                               page_size=page_size)))
                links.append("<{0}>; rel=\"last\""
                             "".format(get_url(page=max_page,
                                               page_size=page_size)))

            headers = {'Link': ", ".join(links)}
            results = query.slice(page * page_size, (page + 1) * page_size)
            return [self._serialize(o) for o in results], 200, headers

        pkg = self._get(obj_id)
        return self._serialize(pkg)

    def post(self):
        new = self.model()
        new.attributes = request.json
        db.session.add(new)
        db.session.commit()
        return self._serialize(new)  # todo: return 201 Created instead?

    def put(self, obj_id):
        obj = self._get(obj_id)
        obj.attributes = request.json
        db.session.commit()

    def patch(self, obj_id):
        obj = self._get(obj_id)
        for key, value in request.json.iteritems():
            if key.startswith('$'):
                ## Custom action -- handle separately
                if key == '$del':
                    for k in value:
                        if k in obj.attributes:
                            del obj.attributes[k]
                elif key == '$set':
                    for k, v in value.iteritems():
                        obj.attributes[k] = v
                else:
                    restful.abort(
                        400, message="Invalid PATCH key: {0}".format(key))
            else:
                obj.attributes[key] = value
        db.session.commit()

    def delete(self, obj_id):
        ## todo: on package deletion, remove resources?
        ## or, safer, disallow deletion if still referenced
        ## -> should be that way by default, btw
        obj = self._get(obj_id)
        db.session.delete(obj)
        db.session.commit()


class PackageResource(ModelResource):
    model = Package


class PackageResourcesResource(ModelResource):
    def _serialize(self, obj):
        serialized = super(PackageResourcesResource, self)._serialize(obj)
        serialized['package_id'] = obj.package_id
        return serialized

    def get(self, obj_id):
        self._query = Package.query.filter_by(id=obj_id).one().resources
        return super(PackageResourcesResource, self).get()

    def post(self, obj_id):
        ## todo: create a resource
        pass


class ResourceResource(ModelResource):
    model = Resource

    def _serialize(self, obj):
        serialized = super(ResourceResource, self)._serialize(obj)
        serialized['package_id'] = obj.package_id
        return serialized


def api_url(rel):
    """Shortcut for generating versioned API URLs"""
    return '/api/1/{0}/'.format(rel)


api.add_resource(PackageResource,
                 api_url('package'),
                 api_url('package/<int:obj_id>'))
api.add_resource(PackageResourcesResource,
                 api_url('package/<int:obj_id>/resources'))
api.add_resource(ResourceResource,
                 api_url('resource'),
                 api_url('resource/<int:obj_id>'))
