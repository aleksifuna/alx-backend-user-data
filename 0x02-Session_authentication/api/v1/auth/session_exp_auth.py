#!/usr/bin/env python3
"""
Module supplies SessionExpAuth class
"""
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
import os


class SessionExpAuth(SessionAuth):
    """
    SessionAuth attributes and methods defination
    """

    def __init__(self):
        """
        Class initialization to overload super class
        """
        expiration_duration = os.getenv('SESSION_DURATION', 0)
        try:
            expiration_duration = int(expiration_duration)
        except Exception:
            expiration_duration = 0
        self.session_duration = expiration_duration

    def create_session(self, user_id=None):
        """
        Creates session and store more information about it
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dictionary = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Returns user_id from session_dictionary
        """
        if session_id is None:
            return None
        session_dictionary = self.user_id_by_session_id.get(session_id)
        if session_dictionary is None:
            return None
        if self.session_duration <= 0:
            return session_dictionary.get('user_id')
        created_at = session_dictionary.get('created_at')
        if created_at is None:
            return None
        session_duration = timedelta(seconds=self.session_duration)
        if created_at + session_duration < datetime.now():
            return None
        return session_dictionary.get('user_id')
