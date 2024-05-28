#!/usr/bin/env python3
"""
Module supplies authentication methods
"""

import bcrypt
from db import DB
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

    def register_user(self, email: str, password: str):
        """Creates a new user and return the instance
        """
        if not email or isinstance(email, str):
            return None
        if not password or isinstance(password, str):
            return None
        try:
            existing_user = self._db.find_user_by(email=email)
            if existing_user:
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            pass
        user = DB.add_user(email=email, password=password)
        return user
