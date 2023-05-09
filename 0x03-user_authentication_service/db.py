#!/usr/bin/env python3
"""
create user
Find user
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import NoResultFound, InvalidRequestError

from user import Base, User


class DB:
    """DB class
    """
    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        A method creates a new instance of the User class with the provided
        email and hashed_password arguments and adds it to the database and
        returns a User object.
        """
        session = self._session
        user = User(email=email, hashed_password=hashed_password)
        session.add(user)
        session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """
        This method takes in an arbitrary keyword arguments and returns the
        first row found in the users table as filtered by the method's input
        arguments.
        """
        session = self._session
        if kwargs is None:
            raise InvalidRequestError

        col_names = User.__table__.columns.keys()
        for i in kwargs.keys():
            if i not in col_names:
                raise InvalidRequestError

        user = session.query(User).filter_by(**kwargs).one()
        if user is None:
            raise NoResultFound
        return user
