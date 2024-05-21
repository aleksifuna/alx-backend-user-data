#!/usr/bin/env python3
"""
Contains class defination for basic_auth
"""
import base64
from api.v1.auth.auth import Auth
from models.user import User
from models.base import DATA
from typing import TypeVar


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
            return decoded_string.decode('utf-8')
        except UnicodeDecodeError:
            return None

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
        split_at = decoded_base64_authorization_header.find(':')
        email = decoded_base64_authorization_header[:split_at]
        password = decoded_base64_authorization_header[split_at + 1:]
        return(email, password)

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str
            ) -> TypeVar('User'):
        """
        Returns the User instance based on the email and password
        """
        if user_email is None:
            return None
        if not isinstance(user_email, str):
            return None
        if user_pwd is None:
            return None
        if not isinstance(user_pwd, str):
            return None
        if 'User' not in DATA:
            return None
        results = User.search({
            'email': user_email
        })
        if len(results) == 0:
            return None
        user = results[0]
        if user.is_valid_password(user_pwd):
            return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves and returns User instance for a request
        """
        auth_header = self.authorization_header(request)
        b64_auth_header = self.extract_base64_authorization_header(auth_header)
        decoded_auth_header = self.decode_base64_authorization_header(
            b64_auth_header
            )
        user_credentials = self.extract_user_credentials(decoded_auth_header)
        user = self.user_object_from_credentials(
            user_credentials[0],
            user_credentials[1]
            )
        return user
