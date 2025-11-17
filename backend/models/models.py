from app import db

class Countries(db.Model):

    __tablename__ = "Countries"
    country_code   = db.Column(db.String(3), nullable=False, primary_key = True)
    country        = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<Country %r>' % (self.country)
    
class Cities(db.Model):

    __tablename__ = "Cities"
    city_code      = db.Column(db.String(3), nullable=False, primary_key = True)
    city           = db.Column(db.String(200), nullable=False)
    country_code   = db.Column(db.String(3), nullable=False, primary_key = True)

    def __repr__(self):
        return '<Country %r>' % (self.country)

class Users(db.Model):

    __tablename__ = "Users"
    username       = db.Column(db.String(100), nullable=False, primary_key = True)
    email          = db.Column(db.String(200), nullable=False)
    phone          = db.Column(db.String(100), nullable=True)
    first_name     = db.Column(db.String(200), nullable=True)
    last_name      = db.Column(db.String(200), nullable=True)
    street_address = db.Column(db.String(200), nullable=True)
    postal_code    = db.Column(db.String(100), nullable=True)
    city_code      = db.Column(db.String(10), nullable=False)
    country_code   = db.Column(db.String(3), nullable=False)
    password       = db.Column(db.String(200), nullable=False)
    salt           = db.Column(db.String(100), nullable=False)
    confirmed      = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return '<User %r>' % (self.username)
