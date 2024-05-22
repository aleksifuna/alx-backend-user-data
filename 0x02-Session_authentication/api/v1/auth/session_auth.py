#!/usr/bin/env python3
"""
Contains SessionAuth class defination
"""

from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """
    SessionAuth cass defination
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Generates SessionID and uses it as key to store user_id
        in the user_id_by_session_id
        """
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Returns a user ID based on a Session ID
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        user_id = self.user_id_by_session_id.get(session_id)
        return user_id
