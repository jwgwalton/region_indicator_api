from enum import IntEnum

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restless import APIManager

# Create the Flask application and the Flask-SQLAlchemy object.
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://postgres:postgres@database:5432/postgres"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # SQLALCHEMY whines about inefficiency if not set
db = SQLAlchemy(app)


# Create your Flask-SQLALchemy models as usual but with the following two
# (reasonable) restrictions:
#   1. They must have a primary key column of type sqlalchemy.Integer orß
#      type sqlalchemy.Unicode.
#   2. They must have an __init__ method which accepts keyword arguments for
#      all columns (the constructor in flask.ext.sqlalchemy.SQLAlchemy.Model
#      supplies such a method, so you don't need to declare a new one).


class NutsRegionLevel(IntEnum):
    NUTS1 = 1
    NUTS2 = 2


class Indicatortype(IntEnum):
    # TODO: put in separate table as will need to be updatable?
    GVA = 0
    GDP = 1


class RegionalIndicator(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nuts_region_id = db.Column(db.Integer) # TODO: static data so put as enum
    nuts_region_level = db.Column(db.Enum(NutsRegionLevel))
    indicator_type = db.Column(db.Enum(Indicatortype))
    indicator_value = db.Column(db.Integer)


# Create the database tables.
db.create_all()

# Create the Flask-Restless API manager.
manager = APIManager(app, flask_sqlalchemy_db=db)

# Create API endpoints, which will be available at /api/<tablename> by
# default. Allowed HTTP methods can be specified as well.
manager.create_api(RegionalIndicator, methods=['GET', 'POST', 'DELETE'], collection_name='indicator')

# start the flask loop
app.run()