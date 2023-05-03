#!/usr/bin/env python3
"""
Basic auth
Basic - Base64 part
"""

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
