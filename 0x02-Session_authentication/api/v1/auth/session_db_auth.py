#!/usr/bin/env python3
""" SessionDBAuth module """
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """ Session authentication with database support """

    def create_session(self, user_id=None):
        """ Create a session and save it in the database """
        session_id = super().create_session(user_id)
        if not session_id:
            return None

        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Retrieve a user ID from the database using the session ID """
        if session_id is None:
            return None

        from models.user_session import UserSession
        UserSession.load_from_file()

        # Search for the session by session_id
        user_sessions = UserSession.search({"session_id": session_id})
        if not user_sessions:
            return None

        # Retrieve the first matching session
        user_session = user_sessions[0]
        if self.session_duration <= 0:
            return user_session.user_id

        # Check if session has expired
        created_at = user_session.created_at
        if not created_at:
            return None

        from datetime import datetime, timedelta
        expiration_time = created_at + timedelta(seconds=self.session_duration)
        if datetime.utcnow() > expiration_time:
            return None

        return user_session.user_id

    def destroy_session(self, request=None):
        """ Destroy a session in the database """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if not session_id:
            return False

        user_sessions = UserSession.search({"session_id": session_id})
        if not user_sessions:
            return False

        user_session = user_sessions[0]
        user_session.remove()
        return True
