from sqlalchemy import Column, Integer, String, DateTime, Boolean, BigInteger, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    password_hash = Column(String)
    created_at = Column(DateTime)
    updated_at= Column(DateTime)
    is_active = Column(Boolean)
    storage_limit = Column(BigInteger)
    storage_used = Column(BigInteger)
    avatar = Column(String)
    
#     image = relationship("Image", back_populates="user")
    
# class Textfile(Base):
#     __tablename__ = "textfiles"

#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#     created_at = Column(DateTime)
#     user_id = Column(Integer, ForeignKey("users.id"))

# class Image(Base):
#     __tablename__ = "images"

#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#     created_at = Column(DateTime)
#     user_id = Column(Integer, ForeignKey("users.id"))