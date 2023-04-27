#!/usr/bin/env python3
"""
Encrypting passwords.
"""

from bcrypt import gensalt, hashpw


def hash_password(password: str) -> bytes:
    """
    This function that expects one string argument name password
    and returns salted, hashed password, which is a byte string.
    """
    salt = gensalt()
    hashed_password = hashpw(password.encode(), salt)

    return hashed_password
