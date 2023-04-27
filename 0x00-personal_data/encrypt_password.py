#!/usr/bin/env python3
"""
Encrypting passwords.
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    This function expects one string argument name password
    and returns salted, hashed password, which is a byte string.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    This function expects 2 arguments and validates the provided password
    with the hashed password and returns a boolean.

    Args:
        hashed_password (bytes): a byte representing hashed password argument.
        password (str): a string representing password argument
    
    Returns:
        bool: True, if it validates correctly.
    """
    return bcrypt.checkpw(password.encode(), hashed_password)