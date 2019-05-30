import math
from ast import literal_eval

from docker.errors import DockerException
from flask_io import fields
from flask_restful import Resource

from web.commons import Setting
from web.commons.docker import DockerClient
from web.commons.pagination import paginate
from web.commons.ssh import ssh_ping, generate_and_save_ssh_key
from web.commons.utils import response
from web.extensions import db, io
from web.models.host import Host
from web.schema.host_schema import HostSchema


def sync_host_info(host_id, uri):
    host_info = DockerClient(base_url=uri).docker_info()
    operate_system = host_info.get('OperatingSystem')
    memory = math.ceil(int(host_info.get('MemTotal')) / 1024 / 1024 / 1024)
    cpu = host_info.get('NCPU')
    # outer_ip = 1
    # inner_ip = 2
    Host.upsert({'host_id': host_id}, host_id=host_id, operate_system=operate_system, memory=memory, cpu=cpu)
    return True


class HostsAPI(Resource):
    @io.from_query('host_query', fields.fields.String())
    def get(self, host_query):
        schema = HostSchema(many=True)
        query = Host.query
        if host_query:
            host_query = literal_eval(host_query)
            if 'name_field' in host_query:
                query = query.filter(Host.name.like('%{}%'.format(host_query['name_field'])))
            if 'zone_field' in host_query:
                query = query.filter(Host.zone.like('%{}%'.format(host_query['zone_field'])))
        return paginate(query, schema)

    @io.from_body(param_name='host', schema=HostSchema)
    @io.marshal_with(HostSchema)
    def post(self, host):
        db.session.add(host)
        db.session.commit()
        return host


class HostAPI(Resource):
    @io.marshal_with(HostSchema)
    def get(self, host_id):
        host = Host.query.get_or_404(host_id)
        return host

    @io.from_body('new_host', HostSchema)
    @io.marshal_with(HostSchema)
    def put(self, host_id, new_host):
        host = Host.query.get_or_404(host_id)
        return new_host

    def delete(self, host_id):
        user = Host.query.get_or_404(host_id)
        db.session.delete(user)
        db.session.commit()
        return response(message='host deleted')


class HostValidAPI(Resource):

    def get(self, host_id):
        host = Host.query.get_or_404(host_id)
        if not Setting.has('ssh_private_key'):
            generate_and_save_ssh_key()
        if ssh_ping(host.ssh_ip, host.ssh_port):
            try:
                sync_host_info(host_id, host.docker_uri)
            except DockerException:
                return response(message='docker fail')
        else:
            return response(message='ssh fail')
        return response()


class HostExecAPI(Resource):
    @io.from_query('tpl_query', fields.fields.String())
    def get(self):
        pass

    def post(self):
        pass
