#!/usr/bin/env python3
"""
Hash password
"""

import bcrypt


def _hash_password(password: str) -> bytes:
    """
    This method takes a password string arguments and returns bytes.
    """
    salted = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salted)
    return hashed_password
