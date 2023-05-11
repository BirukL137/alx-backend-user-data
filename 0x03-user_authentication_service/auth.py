#!/usr/bin/env python3
"""
Hash password
Register user
Credentials validation
Generate UUIDs
Get session ID
Find user by session ID
Destroy session
Generate reset password token
Update password
"""

from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from typing import Union
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

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """
        A method that takes a single session_id string argument. If the
        session ID is None or no user is found, return None. Otherwise return
        the corresponding user.
        """
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        A method that takes a single user_id integer argument and updates the
        corresponding user's session ID to None.
        """
        try:
            user = self._db.find_user_by(id=user_id)
            self._db.update_user(user.id, session_id=None)
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """
        A method that takes an email string as an argument and find the user
        corresponding to the email. If the user exists, it generate a UUID and
        update the user's reset_token database field and return the token.
        Otherwise raise ValueError.
        """
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """
        A method that takes a reset token string argument and a password
        string argument and use the reset token to find the corresponding
        user. If it does exist, it will hash the password and update the
        user's hashed password field with the new one and reset the token to
        None. Otherwise, raises ValueError.
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_password = _hash_password(password)
            self._db.update_user(user.id, hashed_password=hashed_password,
                                 reset_token=None)
        except NoResultFound:
            raise ValueError


def _generate_uuid() -> str:
    """
    A private method that returns a string representation of a new UUID.
    """
    return str(uuid.uuid4())
