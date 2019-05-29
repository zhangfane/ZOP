from flask import Blueprint
from flask_restful import Api

from web.api.resources import UserResource, UserList
from web.api.resources.host import HostsAPI, HostAPI

blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(blueprint)

api.add_resource(UserResource, '/users/<int:user_id>')
api.add_resource(UserList, '/users')
api.add_resource(HostsAPI, '/hosts')
api.add_resource(HostAPI, '/host/<int:host_id>')
