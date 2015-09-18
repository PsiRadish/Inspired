
# from app import db
from models.base import Base, db
from sqlalchemy.orm import reconstructor, validates
from flask.ext.login import UserMixin

class User(Base, UserMixin):
    __tablename__ = 'user'
    
    # ATTRIBUTES
    name            = db.Column(db.String(30), nullable=False, unique=True)
    # gender          = db.Column(db.Enum('female','male','robot','none','fluid','moss'))
    email           = db.Column(db.String, nullable=False, unique=True)
    password        = db.Column(db.String, nullable=False)
    tumblr_key      = db.Column(db.String(50))
    tumblr_secret   = db.Column(db.String(50))
    about           = db.Column(db.Text, default="")
    
    # RELATIONSHIPS
    works = db.relationship("Work", backref="author")
    
    # INITIALIZATION
    # @reconstructor
    # def init_on_load(self):
    #     self.tumblr_oauth = None
    
    # VALIDATION
    @validates('email')
    def validate_email(self, attribute, value):
        assert '@' in value
        return value
    
    # @validates('password')
    # def validate_password(self, attribute, value):
    #     assert len(value) >= 8
    #     return value
    
    def __repr__(self):
        return '\n'.join([
            "id: {}".format(self.id),
            "  name: {}".format(self.name),
            "  email: {}".format(self.email)])
