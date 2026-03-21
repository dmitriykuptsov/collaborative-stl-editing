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
    enable_two_factor_auth = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return '<User %r>' % (self.username)

class TwoFactorAuthentication(db.Model):
    __tablename__  = "TwoFactorAuthentication"

    username       = db.Column(db.String(100), nullable=False, primary_key=True)
    code           = db.Column(db.String(6), nullable=False, primary_key=True)
    exp            = db.Column(db.Integer, default=0)

class ConfirmationTokens(db.Model):
    __tablename__  = "ConfirmationTokens"

    username       = db.Column(db.String(100), nullable=False, primary_key=True)
    token          = db.Column(db.String(100), nullable=False, primary_key=True)
    exp            = db.Column(db.Integer, default=0)

class Objects(db.Model):
    __tablename__  = "Objects"
    
    object         = db.Column(db.String(400), nullable=False, primary_key=True)
    owner          = db.Column(db.String(100), nullable=False, primary_key=True)
    description    = db.Column(db.String(4000), nullable=True)
    creation_time  = db.Column(db.Date, nullable=False)

class ObjectVersions(db.Model):
    __tablename__  = "ObjectVersions"

    object                     = db.Column(db.String(400), nullable=False, primary_key=True)
    version                    = db.Column(db.Integer, nullable=False, primary_key=True)
    owner                      = db.Column(db.String(100), nullable=False, primary_key=True)
    hash                       = db.Column(db.String(200), nullable=False)
    date_uploaded              = db.Column(db.Date, nullable=False)
    surface_area               = db.Column(db.Float(10, 10))
    volume                     = db.Column(db.Float(10, 10))
    cog_x                      = db.Column(db.Float(10, 10))
    cog_y                      = db.Column(db.Float(10, 10))
    cog_z                      = db.Column(db.Float(10, 10))
    bb_x_l                     = db.Column(db.Float(10, 10))
    bb_y_l                     = db.Column(db.Float(10, 10))
    bb_z_l                     = db.Column(db.Float(10, 10))
    bb_x_h                     = db.Column(db.Float(10, 10))
    bb_y_h                     = db.Column(db.Float(10, 10))
    bb_z_h                     = db.Column(db.Float(10, 10))
    is_water_tight             = db.Column(db.Boolean, default=True)
    number_of_facets           = db.Column(db.Integer)
    number_of_unique_edges     = db.Column(db.Integer)
    number_of_unique_verticies = db.Column(db.Integer)
    has_zero_area_triangles    = db.Column(db.Boolean)
    is_edge_manifold           = db.Column(db.Boolean)
    is_vertex_manifold         = db.Column(db.Boolean)


class Colors(db.Model):
    __tablename__  = "Colors"
    
    color          = db.Column(db.String(100), nullable=False, primary_key=True)

class Materials(db.Model):
    __tablename__  = "Materials"

    material            = db.Column(db.String(100), nullable=False, primary_key=True)
    type_code           = db.Column(db.Integer, nullable=False)
    color               = db.Column(db.String(100), nullable=False, primary_key=True)
    price_per_cubic_cm  = db.Column(db.Float(10, 10), nullable=False, default=0)

class Machinery(db.Model):
    __tablename__  = "Machinery"

    machine             = db.Column(db.String(100), nullable=False, primary_key=True)

    dimension_x         = db.Column(db.Float(10, 10), nullable=False)
    dimension_y         = db.Column(db.Float(10, 10), nullable=False)
    dimension_z         = db.Column(db.Float(10, 10), nullable=False)

    material            = db.Column(db.String(100), nullable=False, primary_key=True)
    color               = db.Column(db.String(100), nullable=False, primary_key=True)

class Providers(db.Model):
    __tablename__  = "Providers"

    provider            = db.Column(db.String(400), nullable=False, primary_key=True)
    is_local            = db.Column(db.Boolean, default=True)

class ProvidersMachinery(db.Model):

    __tablename__  = "ProvidersMachinery"

    provider            = db.Column(db.String(400), nullable=False, primary_key=True)
    machine             = db.Column(db.String(100), nullable=False, primary_key=True)
    material            = db.Column(db.String(100), nullable=False, primary_key=True)
    color               = db.Column(db.String(100), nullable=False, primary_key=True)

class OrderStatus(db.Model):
    __tablename__  = "OrderStatus"

    status              = db.Column(db.String(100), nullable=False, primary_key=True)

class Orders(db.Model):
    __tablename__  = "Orders"

    order_number        = db.Column(db.String(100), nullable=False, primary_key=True)
    version             = db.Column(db.Integer, nullable=False)
    owner               = db.Column(db.String(100), nullable=False)
    status              = db.Column(db.String(100), nullable=False)
    paid                = db.Column(db.Boolean, default=False)
    cost                = db.Column(db.Float(10, 10))
    object              = db.Column(db.String(100), nullable=False)
    machine             = db.Column(db.String(100), nullable=False)
    material            = db.Column(db.String(100), nullable=False)
    color               = db.Column(db.String(100), nullable=False)
    order_date          = db.Column(db.Date, nullable=False)


class Permissions(db.Model):
    __tablename__  = "Permissions"

    permission          = db.Column(db.String(10), nullable=False, primary_key=True)
    description         = db.Column(db.String(100), nullable=False)

class Shares(db.Model):
    __tablename__  = "Shares"

    object              = db.Column(db.String(100), nullable=False, primary_key=True)
    username            = db.Column(db.String(100), nullable=False, primary_key=True)
    owner               = db.Column(db.String(100), nullable=False, primary_key=True)
    permission          = db.Column(db.String(10))

class Comments(db.Model):
    __tablename__  = "Comments"

    object              = db.Column(db.String(100), nullable=False, primary_key=True)
    username            = db.Column(db.String(100), nullable=False, primary_key=True)
    owner               = db.Column(db.String(100), nullable=False, primary_key=True)
    comment             = db.Column(db.Text)
    date_of_comment     = db.Column(db.Date)
