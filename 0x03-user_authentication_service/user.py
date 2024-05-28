#!/usr/bin/env python3
"""
Module for SQLalchemy model named User for a database table named users
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Sequence

Base = declarative_base()


class User(Base):
    """
    User SQLalchemy model defination
    """
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id'), primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)

    def __init__(self, **kwargs):
        """
        Initializes the class instance
        """
        for key, value in kwargs.items():
            setattr(self, key, value)