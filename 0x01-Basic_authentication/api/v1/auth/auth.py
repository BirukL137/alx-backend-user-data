#!/usr/bin/env python3
"""
Auth class
"""

from flask import request
from typing import List, TypeVar


class Auth:
    """ Authentication class """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ checks if it requires authorization """
        if path is None or excluded_paths is None or excluded_paths == []:
            return True
        else:
            return False

    def authorization_header(self, request=None) -> str:
        """ Returns authorization header request object """
        if request is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """ Returns current user request object """
        return None
