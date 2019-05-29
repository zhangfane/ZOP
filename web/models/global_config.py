from web.extensions import db


class GlobalConfig(db.Model):
    __tablename__ = 'setting_config'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    desc = db.Column(db.String(255))
    value = db.Column(db.Text)

    def __repr__(self):
        return '<GlobalConfig %r>' % self.name
