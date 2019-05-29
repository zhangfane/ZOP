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

    def __repr__(self):
        return '<Host %r>' % self.name
