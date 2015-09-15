# print("8")

from app import db
from sqlalchemy.orm import validates

class User(db.Model):
    __tablename__ = 'user'

    id              = db.Column(db.Integer, primary_key=True)
    name            = db.Column(db.String(30), nullable=False, unique=True)
    email           = db.Column(db.String, nullable=False, unique=True)
    password        = db.Column(db.String(30), nullable=False)
    # gender          = db.Column(db.Enum('female','male','robot','none','fluid','moss'))
    tumblr_key      = db.Column(db.String(50))
    tumblr_secret   = db.Column(db.String(50))
    
    # print("9")
    
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
    
    