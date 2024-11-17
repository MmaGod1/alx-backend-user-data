#!/usr/bin/env python3
"""Session Expiration Authentication module."""
import os
from datetime import datetime, timedelta
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """Session authentication with expiration."""

    def __init__(self):
        """Initialize the instance with session duration."""
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION', 0))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """Create a session ID and store session details."""
        session_id = super().create_session(user_id)
        if not session_id:
            return None

        session_dict = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dict
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Retrieve a user ID for a session ID, considering expiration."""
        if session_id is None:
            return None

        session_dict = self.user_id_by_session_id.get(session_id)
        if not session_dict:
            return None

        user_id = session_dict.get("user_id")
        created_at = session_dict.get("created_at")

        if self.session_duration <= 0:
            return user_id

        if not created_at:
            return None

        expiration_time = created_at + timedelta(seconds=self.session_duration)
        if datetime.now() > expiration_time:
            return None

        return user_id
