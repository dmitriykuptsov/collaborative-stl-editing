from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as db

from config import SQLALCHEMY_DATABASE_URI

base = declarative_base()
engine = db.create_engine(SQLALCHEMY_DATABASE_URI)
base.metadata.bind = engine
session = orm.scoped_session(orm.sessionmaker())(bind=engine)

class Objects(base):
    __tablename__  = "Objects"
    
    object         = db.Column(db.String(400), nullable=False, primary_key=True)
    owner          = db.Column(db.String(100), nullable=False, primary_key=True)
    description    = db.Column(db.String(4000), nullable=True)
    creation_time  = db.Column(db.Date, nullable=False)

class ObjectVersions(base):
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
    number_of_unique_verticies = db.Column(db.Integer)
    has_zero_area_triangles    = db.Column(db.Boolean)
    is_edge_manifold           = db.Column(db.Boolean)
    is_vertex_manifold         = db.Column(db.Boolean)


