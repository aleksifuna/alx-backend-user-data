#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import NoResultFound
from typing import Dict

from user import Base
from user import User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Creates and returns a user object
        """
        user = User(
            email=email,
            hashed_password=hashed_password
        )
        session = self._session
        session.add(user)
        session.commit()
        return user

    def find_user_by(self, **kwargs: Dict) -> User:
        """Searches for a row matching attributes in kwargs dict
        """
        session = self._session
        user = session.query(User).filter_by(**kwargs).first()
        if user:
            return user
        else:
            raise NoResultFound

    def update_user(self, user_id: int, **kwargs: Dict) -> None:
        """Updates user with user_id as id with **kwargs
        """
        try:
            user = self.find_user_by(id=user_id)
        except Exception:
            raise Exception
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
            else:
                raise ValueError
        self._session.commit()
        return None