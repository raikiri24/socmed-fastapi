from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from configs.db import Base
import datetime
import pytz


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    phone_number = Column(String)
    posts = relationship("Posts", back_populates="owner")


class Posts(Base):
    __tablename__ = "posts"
    timezone = pytz.timezone('Asia/Manila')

    ph_date_time = datetime.datetime.now(timezone)

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)

    owner_id = Column(Integer, ForeignKey("users.id"))
    created_date = Column(DateTime, default=ph_date_time)
    updated_date = Column(DateTime, default=ph_date_time)
    deleted_date = Column(DateTime, nullable=True)
    owner = relationship("Users", back_populates="posts")
