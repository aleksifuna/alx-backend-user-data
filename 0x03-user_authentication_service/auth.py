#!/usr/bin/env python3
"""
Module supplies authentication methods
"""

import bcrypt
from db import DB, User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """Hashes a password string and return bytes representation
    """
    byte_pw = password.encode('utf-8')
    hashed_pw = bcrypt.hashpw(byte_pw, bcrypt.gensalt())
    return hashed_pw


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """ Class constructor
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Creates a new user and return the instance
        """
        if not email or not isinstance(email, str):
            raise None
        if not password or not isinstance(password, str):
            return None
        try:
            existing_user = self._db.find_user_by(email=email)
            if existing_user:
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            pass
        hashed_password = _hash_password(password)
        user = self._db.add_user(
            email=email,
            hashed_password=hashed_password
            )
        return user
