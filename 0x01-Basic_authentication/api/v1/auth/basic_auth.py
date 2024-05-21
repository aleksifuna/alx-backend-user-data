#!/usr/bin/env python3
"""
Contains class defination for basic_auth
"""

from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """
    Class defination for basicAuth
    """

    def extract_base64_authorization_header(
            self,
            authorization_header: str
            ) -> str:
        """
        Extracts the base64 authorization from the header
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        base64_string = authorization_header.split(' ')
        return base64_string[1]
