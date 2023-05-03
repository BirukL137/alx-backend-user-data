#!/usr/bin/env python3
"""
Basic auth
Basic - Base64 part
Basic - Base64 decode
"""

import base64
from api.v1.auth.auth import Auth


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
