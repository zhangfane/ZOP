from web.extensions import db


class Host(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    desc = db.Column(db.String(255))
    type = db.Column(db.String(50))
    zone = db.Column(db.String(50))
    docker_uri = db.Column(db.String(255))
    ssh_ip = db.Column(db.String(32))
    ssh_port = db.Column(db.Integer)

    operate_system = db.Column(db.String(64))
    memory = db.Column(db.SmallInteger)
    cpu = db.Column(db.SmallInteger)
    disk = db.Column(db.SmallInteger)
    outer_ip = db.Column(db.String(128))
    inner_ip = db.Column(db.String(128))

    def __repr__(self):
        return '<Host %r>' % self.name


class HostExecTemplate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tpl_name = db.Column(db.String(50))
    tpl_desc = db.Column(db.String(255))
    tpl_type = db.Column(db.String(50))
    tpl_content = db.Column(db.Text())

    def __repr__(self):
        return '<HostExecTemplate %r>' % self.tpl_name
