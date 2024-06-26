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
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        for link in excluded_paths:
            if link.endswith('*') and path.startswith(link[:-1]):
                return False
            elif path in link:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """ Creates and return a string for the authorization header
        """
        if request is None:
            return None
        authorization = request.headers.get('Authorization')
        if authorization:
            return authorization
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ returns the current user
        """
        return None
