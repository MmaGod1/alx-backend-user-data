#!/usr/bin/env python3
""" Session Authentication Module.
"""
from .auth import Auth


class SessionAuth():
    """ Session Authentication mechanism."""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ Creates the session ID"""
        if user_id is None:
            return None
        if isinstance(user_id, str) is None:
            return None

        session_id = uuid.uuid4()
        user_id_by_session_id[session_id] = user_id
        return session_id
