from app import db

class Users(db.Model):

    __tablename__ = "Users"
    username  = db.Column(db.String(100), nullable=False, primary_key = True)
    email     = db.Column(db.String(200), nullable=False)
    password  = db.Column(db.String(200), nullable=False)
    salt      = db.Column(db.String(100), nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return '<User %r>' % (self.username)
