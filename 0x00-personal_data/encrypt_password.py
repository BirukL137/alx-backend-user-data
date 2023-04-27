#!/usr/bin/env python3
"""
Encrypting passwords.
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    This function that expects one string argument name password
    and returns salted, hashed password, which is a byte string.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password
