#!/usr/bin/env python3
"""
Auth module to handle password hashing
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """
    Hash a password with a salt using bcrypt
    Args:
        password (str): The password to hash
    Returns:
        bytes: The salted hash of the password
    """
    salt = bcrypt.gensalt()

    # Hash the password with the salt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a new user after checking if they already exist."""
        try:
            # Try to find if user already exists
            self._db.find_user_by(email=email)
            raise ValueError
        except NoResultFound:
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email, hashed_password)
            return new_user
