#!/usr/bin/env python3
"""
Module supplies authentication methods
"""

import bcrypt
import uuid
from db import DB, User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError


def _hash_password(password: str) -> bytes:
    """Hashes a password string and return bytes representation
    """
    byte_pw = password.encode('utf-8')
    hashed_pw = bcrypt.hashpw(byte_pw, bcrypt.gensalt())
    return hashed_pw


def _generate_uuid() -> str:
    """Generates uuid code and return a string representation
    """
    return str(uuid.uuid4())


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

    def valid_login(self, email: str, password: str) -> bool:
        """Authenticates a user with email and password provides
        """
        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
                return True
            return False
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """Creates a session for user corresponding to email
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                session_id = _generate_uuid()
                self._db.update_user(user.id, session_id=session_id)
                return user.session_id
            return None
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str):
        """Return a corresponding user to session_id or None
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None
        except InvalidRequestError:
            return None
