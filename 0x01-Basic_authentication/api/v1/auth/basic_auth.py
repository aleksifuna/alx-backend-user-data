#!/usr/bin/env python3
"""
Contains class defination for basic_auth
"""
import base64
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

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str
            ) -> str:
        """
        Decodes a base64 authorization header to returns a string equivalent
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_string = base64.b64decode(base64_authorization_header)
        except ValueError:
            return None
        return decoded_string.decode('utf-8')

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str
            ) -> (str, str):
        """
        Returns the user email and password from the base64 decoded value
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        user_credentials = decoded_base64_authorization_header.split(':')
        return(user_credentials[0], user_credentials[1])
