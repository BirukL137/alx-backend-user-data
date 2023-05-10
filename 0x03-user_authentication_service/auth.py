#!/usr/bin/env python3
"""
Hash password
Register user
Credentials validation
Generate UUIDs
Get session ID
"""

from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import bcrypt
import uuid


def _hash_password(password: str) -> bytes:
    """
    This method takes a password string arguments and returns bytes.
    """
    salted = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salted)
    return hashed_password


class Auth:
    """Auth class to interact with the authentication database.
    """
    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        This method takes mandatory email and password string arguments
        and returns a User object. If a user already exists with the passed
        email, it raises a ValueError. Otherwise, it hashes the password with
        _hash_password, saves the user to the database and returns the User
        object.
        """
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email=email,
                                     hashed_password=hashed_password)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """
        This method expects email and password required arguments and returns
        a boolean. It tries locating the user by email. If it exists, it
        checks the password, If it matches, it returns True. Otherwise False.
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode('utf-8'),
                                  user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """
        A method takes an email string argument and returns the Session ID
        as a string.
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None


def _generate_uuid() -> str:
    """
    A private method that returns a string representation of a new UUID.
    """
    return str(uuid.uuid4())
