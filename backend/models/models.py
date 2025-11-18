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
        return '<Cities %r>' % (self.city)

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

class ConfirmationTokens(db.Model):
    __tablename__  = "ConfirmationTokens"

    username       = db.Column(db.String(100), nullable=False, primary_key=True)
    token          = db.Column(db.String(100), nullable=False)
    exp            = db.Column(db.Integer, default=0)

class Objects(db.Model):
    __tablename__  = "Objects"
    
    name           = db.Column(db.String(400), nullable=False, primary_key=True)
    owner          = db.Column(db.String(100), nullable=False, primary_key=True)
    description    = db.Column(db.String(2000), nullable=True)
    creation_time  = db.Column(db.Date, nullable=False)

class ObjectVersions(db.Model):
    __tablename__  = "ObjectVersions"

    name           = db.Column(db.String(400), nullable=False, primary_key=True)
    version        = db.Column(db.Integer, nullable=False)
    owner          = db.Column(db.String(100), nullable=False)
    hash           = db.Column(db.String(200), nullable=False)
    model_file     = db.Column(db.LargeBinary, nullable=False)
    date_uploaded  = db.Column(db.Date, nullable=False)
    volume         = db.Column(db.Float(10, 10))
    cog_x          = db.Column(db.Float(10, 10))
    cog_y          = db.Column(db.Float(10, 10))
    cog_z          = db.Column(db.Float(10, 10))
    is_water_tight = db.Column(db.Boolean, default=True)
    number_of_facets = db.Column(db.Integer)
    number_of_unique_verticies = db.Column(db.Integer)
    has_zero_area_triangles = db.Column(db.Boolean)
    is_edge_manifold = db.Column(db.Boolean)
    is_vertex_manifold = db.Column(db.Boolean)