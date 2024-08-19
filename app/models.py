from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    interests = db.relationship("Interest", backref="user", lazy=True)


class Interest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)
    value = db.Column(db.String(100), nullable=False)
    threshold = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


class Content(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    tags = db.relationship("Tag", backref="content", lazy=True)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)
    value = db.Column(db.String(100), nullable=False)
    threshold = db.Column(db.Float, nullable=False)
    content_id = db.Column(db.String(50), db.ForeignKey("content.id"), nullable=False)
