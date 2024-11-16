#!/usr/bin/env python3
""" Session Authentication Module.
"""
from .auth import Auth
import uuid

class SessionAuth:
    """ Session Authentication mechanism."""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Create a session ID for a given user ID.
            Return: the session ID.
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Returns a User ID based on asession_id or,
            None if session_id is None or not a string.
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)
    
