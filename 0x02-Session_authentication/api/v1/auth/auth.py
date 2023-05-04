#!/usr/bin/env python3
"""
Auth class
"""

from flask import Flask, request
from typing import List, TypeVar
from os import getenv


class Auth:
    """ Authentication class """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ checks if it requires authorization """
        if path is None:
            return True
        elif excluded_paths is None or excluded_paths == []:
            return True
        elif path in excluded_paths:
            return False
        else:
            for k in excluded_paths:
                if k.startswith(path):
                    return False
                if path.startswith(k):
                    return False
                if k[-1] == "*":
                    if path.startswith(k[:-1]):
                        return False
        return True

    def authorization_header(self, request=None) -> str:
        """ Returns authorization header request object """
        if request is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """ Returns current user request object """
        request = Flask(__name__)
        return None

    def session_cookie(self, request=None):
        """
        Returns a cookie value from a request.
        """
        if request is None:
            return None

        if getenv('SESSION_NAME') is None:
            return None

        return request.cookies.get(getenv('SESSION_NAME'))
