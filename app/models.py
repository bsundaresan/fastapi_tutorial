from .database import Base

from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text

# SQLAlchemy will not alter pre existing tables so if you need to
# change the models then the preexisting table would have to be
# deleted first. It can be done using Alembic 

class Post(Base):
    """
    These are models similar to the one used in Django and Flask.
    The idea is to use a ORM to build tables on the fly and not rely on 
    CLI or PGAdmin to do the same.
    The inheritence is from the Base class of SQLAlchemy that will provide
    the Post class with th required ORM methods
    """
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'),nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    #relationship returns the User using the owner_id 
    owner = relationship("User")

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'),nullable=False)

class Vote(Base):
    __tablename__ = 'votes'

    user_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete='CASCADE'), primary_key=True)



