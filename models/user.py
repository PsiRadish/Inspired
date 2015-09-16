# print("8")

print(__name__, '0')

from app import db
from sqlalchemy.orm import validates
from flask.ext.security import UserMixin, RoleMixin

print(__name__, '1')

class Role(db.Model, RoleMixin):  # Roles implemented only because Flask-Security seems to require it
    __tablename__ = 'role'
    
    id              = db.Column(db.Integer(), primary_key=True)
    name            = db.Column(db.String(80), unique=True)
    description     = db.Column(db.String(255))

print(__name__, '2')

# Join table
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

print(__name__, '3')

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id              = db.Column(db.Integer, primary_key=True)
    name            = db.Column(db.String(30), nullable=False, unique=True)
    # gender          = db.Column(db.Enum('female','male','robot','none','fluid','moss'))
    email           = db.Column(db.String, nullable=False, unique=True)
    password        = db.Column(db.String(30), nullable=False)
    tumblr_key      = db.Column(db.String(50))
    tumblr_secret   = db.Column(db.String(50))
    
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))
    
    @validates('email')
    def validate_email(self, attribute, value):
        assert '@' in value
        return value
        
    @validates('password')
    def validate_password(self, attribute, value):
        assert len(value) >= 8
        return value
    
    # def __init__(self):
    #     stuff
    # print("10")
    
    def __repr__(self):
        return '\n'.join(
            "id: {}".format(self.id),
            "  name: {}".format(self.name),
            "  email: {}".format(self.email))

print(__name__, '4')
