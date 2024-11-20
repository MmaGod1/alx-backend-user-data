#!/usr/bin/env python3
"""
Auth module to handle password hashing
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


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

def _generate_uuid() -> str:
    """
    Generate a uuid and return its string representation
    """
    return str(uuid4())

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

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validates a user's login credentials.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False

        user_password = user.hashed_password
        pswd = password.encode("utf-8")
        return bcrypt.checkpw(pswd, user_password)

    def create_session(self, email: str) -> str:
        """Creates a session for the user, generates a session ID,
        and stores it in the database.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        # generate a new session ID.
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str):
        """
        Returns the user corresponding to the given session_id.
        """
        if session_id is None:
            return None

        user = self._db.find_user_by(session_id=session_id)
        return user if user else None
