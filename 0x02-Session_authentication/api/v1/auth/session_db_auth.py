#!/usr/bin/env python3
"""
SessionDBAuth module
"""

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """
    Class attributes and methods defination
    """
    def create_session(self, user_id=None):
        """
        Creates and stores new instance of UserSession and return
        the session ID
        """
        if user_id is None or not isinstance(user_id, str):
            return None
        user_session = UserSession()
        user_session.user_id = user_id
        user_session.save()
        return user_session.session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Returns the user_id relates to the session_id
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        session_search = []
        try:
            session_search = UserSession.search({
                'session_id': session_id
                })
        except Exception:
            return None
        if len(session_search) == 0:
            return None
        user_session = session_search[0]
        if self.session_duration <= 0:
            return user_session.user_id
        created_at = user_session.created_at
        session_duration = timedelta(seconds=self.session_duration)
        if (created_at + session_duration) < datetime.now():
            return None
        return user_session.user_id

    def destroy_session(self, request=None):
        """
        Destroys the userSession based on the session ID from the
        request cookie
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_session = UserSession.get(session_id)
        if user_session is None:
            return False
        user_session.remove()
        return True
