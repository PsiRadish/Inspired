
print(__name__, '0')

# from app import db
from models.base import Base, db
from sqlalchemy.orm import validates
from sqlalchemy.dialects import postgresql

class Work(Base):
    __tablename__ = 'work'
    
    # ATTRIBUTES
    title           = db.Column(db.String, nullable=False)
    # no time for proper tags, we'll just fake it with Postgres arrays
    fandom_tags     = db.Column(postgresql.ARRAY(db.String), nullable=False)
    content_tags    = db.Column(postgresql.ARRAY(db.String))
    char_tags       = db.Column(postgresql.ARRAY(db.String))
    ship_tags       = db.Column(postgresql.ARRAY(db.String))
    
    # RELATIONSHIPS
    author_id       = db.Column(db.Integer, db.ForeignKey('user.id')) # one author per work for now
    chapters        = db.relationship("Chapter", backref="work")
    
    @validates('title')
    def validate_title(self, attribute, value):
        assert len(value) >= 1
        return value

class Chapter(Base):
    __tablename__ = 'chapter'
    
    #ATTRIBUTES
    title           = db.Column(db.String, nullable=False)
    order           = db.Column(db.Integer, nullable=False)
    numeral         = db.Column(db.String, nullable=False)
    body            = db.Column(db.Text, nullable=False)
    
    #RELATIONSHIPS
    work_id         = db.Column(db.Integer, db.ForeignKey('work.id'))
    
    @validates('body')
    def validate_body(self, attribute, value):
        assert len(value) >= 1
        return value
