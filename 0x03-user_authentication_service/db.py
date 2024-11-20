#!/usr/bin/env python3
""" DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from user import Base, User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError


class DB:
    """DB class"""

    def __init__(self) -> None:
        """Initialize a new DB instance"""
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object"""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Create a new user and save it to the database
        Args:
            email (str): user's email address
            hashed_password (str): user hashed password
        Return: the User object
        """
        new_user = User(email=email, hashed_password=hashed_password)
        # Add user to the session
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
        Finds a user in the database based on arbitrary keyword arguments.
        Args:
            **kwargs: Arbitrary keyword arguments to filter users.
        Returns:
            User: The first user matching the criteria.
        Raises:
            NoResultFound: If no user matches the criteria.
            InvalidRequestError: If invalid query arguments are provided.
        """
        try:
            # Use filter_by to query with kwargs
            user = self._session.query(User).filter_by(**kwargs).first()
            if user is None:
                raise NoResultFound
            return user
        except AttributeError:
            raise InvalidRequestError

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Update a user's attributes based on the user_id and keyword arguments.
        Args:
            user_id (int): The user's ID to update.
            **kwargs: Arbitrary keyword arguments to update user attributes.
        Raises:
            ValueError: If an invalid attribute is provided.
        """
        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            # Check if the key is a valid attribute of User
            if not hasattr(user, key):
                raise ValueError
            setattr(user, key, value)
        self._session.commit()
