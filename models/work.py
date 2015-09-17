
from app import db
from models.base import Base
from sqlalchemy.dialects.postgresql import JSON # no time for proper tags, so we'll hack some lists in with JSON

class Work(Base):
    __tablename__ = 'work'
    
    