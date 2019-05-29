from ast import literal_eval

from flask import request
from flask_io import fields
from flask_restful import Resource

from web.commons import Setting
from web.commons.pagination import paginate
from web.extensions import ma, db, io
from web.models.host import Host


class HostSchema(ma.ModelSchema):
    class Meta:
        model = Host


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
        return {"msg": "host deleted"}


class HostValid(Resource):

    def get(self, host_id):
        cli = Host.query.get_or_404(host_id)
        if not Setting.has('ssh_private_key'):
            generate_and_save_ssh_key()
        if ssh.ssh_ping(cli.ssh_ip, cli.ssh_port):
            try:
                sync_host_info(host_id, cli.docker_uri)
            except DockerException:
                return json_response(message='docker fail')
        else:
            return json_response(message='ssh fail')
        return json_response()
        pass
