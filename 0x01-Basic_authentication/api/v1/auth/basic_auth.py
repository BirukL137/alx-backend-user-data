#!/usr/bin/env python3
"""
Basic auth
Basic - Base64 part
Basic - Base64 decode
Basic - User credentials
Basic - User object
Basic - Overload current_user - and BOOM!
"""

import base64
from api.v1.auth.auth import Auth
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """ BasicAuth class that inherits from parent Auth class. """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        Extracts the Base64 part of the Authorization header
        for a Basic Authentication.
        """
        if authorization_header is None or \
            not isinstance(authorization_header, str) or \
                not authorization_header.startswith("Basic "):
            return None
        return authorization_header.split(" ")[1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        Decodes a Base64 string and Returns None,
        if base64_authorization_header is None or not a string or
        not a valid Base64.
        """
        base = base64_authorization_header
        if base is None or not isinstance(base, str):
            return None
        try:
            return base64.b64decode(base).decode('utf-8')
        except BaseException:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """
        Extracts the user email and password from the Base64 decoded value and
        returns tuple, The user email and password separated by a colon.
        """
        if decoded_base64_authorization_header is None or \
            not isinstance(decoded_base64_authorization_header, str) or \
                ':' not in decoded_base64_authorization_header:
            return None, None
        return tuple(decoded_base64_authorization_header.split(':'))

    def user_object_from_credentials(self,
                                     user_email: str, user_pwd: str
                                     ) -> TypeVar('User'):
        """
        Returns User instance if email and password are valid, None otherwise.
        """
        if not isinstance(user_email, str) or not isinstance(user_pwd, str):
            return None

        users = User.search({'email': user_email})
        if not users:
            return None

        for user in users:
            if user.is_valid_password(user_pwd):
                return user

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        This function retrieves the User instance for a request and
        returns User instance if request is authorized, None otherwise.
        """
        if not request:
            return None

        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None

        encoded_cred = self.extract_base64_authorization_header(auth_header)
        if not encoded_cred:
            return None

        decoded_cred = self.decode_base64_authorization_header(encoded_cred)
        if not decoded_cred:
            return None

        user_email, user_pwd = self.extract_user_credentials(decoded_cred)
        if not user_email or not user_pwd:
            return None

        user = self.user_object_from_credentials(user_email=user_email,
                                                 user_pwd=user_pwd)
        return user
