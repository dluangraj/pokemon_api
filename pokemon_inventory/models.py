from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid 
from datetime import datetime

# add Flask security passwords
from werkzeug.security import generate_password_hash, check_password_hash

# import for Secrets module(given by Python)
import secrets

# import for Login Manager
from flask_login import UserMixin

# import for Flask Login
from flask_login import LoginManager

# import for Flask-Marshmallow
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# make sure to add in UserMixin to User class
class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default = '')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String(150), nullable = True, default = '')
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default = '', unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __init__(self, email, first_name = '', last_name = '', id = '', password = '', token = '', g_auth_verify = False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_token(self, length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f"User {self.email} has been added to the database!"

class Species(db.Model):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(150))
    national_dex_number = db.Column(db.Numeric(10))
    generation = db.Column(db.Numeric(10))
    types = db.Column(db.String(150))
    abilities = db.Column(db.String(150))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, name, national_dex_number, generation, types, abilities, user_token, id = ''):
        self.id = self.set_id()
        self.name = name
        self.national_dex_number = national_dex_number
        self.generation = generation
        self.types = types
        self.abilities = abilities
        self.user_token = user_token

    def __repr__(self):
        return f"The following Species has been added: {self.name}"

    def set_id(self):
        return (secrets.token_urlsafe())

# creation of API Schema via the Marshmallow Object
class SpeciesSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name', 'national_dex_number', 'generation', 'types', 'abilities']

species_schema = SpeciesSchema()
speciess_schema = SpeciesSchema(many = True)
