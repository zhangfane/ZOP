from marshmallow import fields

from web.extensions import ma


class HostSchema(ma.Schema):
    id = fields.Integer(load_only=True)
    name = fields.String(required=True)
    desc = fields.String(required=True)
    type = fields.String(required=True)
    zone = fields.String(required=True)
    docker_uri = fields.String(required=True)
    ssh_ip = fields.String(required=True)
    ssh_port = fields.Integer(required=True)
    operate_system = fields.String()
    memory = fields.Integer()
    cpu = fields.Integer()
    disk = fields.Integer()
    outer_ip = fields.String()
    inner_ip = fields.String()
    # class Meta:
    #     model = Host


class HostExecSchema(ma.ModelSchema):
    pass
