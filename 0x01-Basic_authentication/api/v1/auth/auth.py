#!/usr/bin/env python3
"""
Contains Auth class defination
"""

from flask import request
from typing import List, TypeVar


class Auth:
    """
    Defines class Auth
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Checks if path requires authentication
        """
        return False

    def authorization_header(self, request=None) -> str:
        """ Creates and return a string for the authorization header
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ returns the current user
        """
        return None
