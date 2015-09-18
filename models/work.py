
print(__name__, '0')

# from app import db
from models.base import Base, db
from sqlalchemy.orm import validates, backref
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.orderinglist import ordering_list

class Work(Base):
    __tablename__ = 'work'
    
    # ATTRIBUTES
    title           = db.Column(db.String, nullable=False)
    summary         = db.Column(db.Text, nullable=False)
    # no time for proper tags, we'll just fake it with Postgres arrays
    fandom_tags     = db.Column(postgresql.ARRAY(db.String), nullable=False)
    content_tags    = db.Column(postgresql.ARRAY(db.String))
    char_tags       = db.Column(postgresql.ARRAY(db.String))
    ship_tags       = db.Column(postgresql.ARRAY(db.String))
    
    # RELATIONSHIPS
    author_id       = db.Column(db.Integer, db.ForeignKey('user.id')) # one author per work for now
    chapters        = db.relationship("Chapter", order_by="Chapter.position", backref="work",
                      collection_class=ordering_list('position'))#, cascade='all, delete-orphan', passive_deletes=True)
    
    @validates('title')
    def validate_title(self, attribute, value):
        assert len(value) >= 1
        return value


class Chapter(Base):
    __tablename__ = 'chapter'
    
    #ATTRIBUTES
    title           = db.Column(db.String, nullable=False)
    position        = db.Column(db.Integer)#, nullable=False)
    numeral         = db.Column(db.String, nullable=False)
    body            = db.Column(db.Text, nullable=False)
    
    #RELATIONSHIPS
    work_id         = db.Column(db.Integer, db.ForeignKey('work.id'))
                    # best as I can tell, this should make the 'position' attribute auto-increment per chapter per work
    # work            = db.relationship('Work', backref=backref('chapters', order_by='Chapter.position',
    #                     collection_class=ordering_list('position'),
    #                     cascade='all, delete-orphan', passive_deletes=True)) # delete chapters when work is deleted
    
    #VALIDATION
    @validates('body')
    def validate_body(self, attribute, value):
        assert len(value) >= 1
        return value
