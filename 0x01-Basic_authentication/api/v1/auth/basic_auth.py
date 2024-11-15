#!/usr/bin/env python3
""" Basic Authentication Module.
"""
from .auth import Auth


class BasicAuth(Auth):
    """ Inherits fro Auth class and
    performes a Basic Authentication.
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        Returns:
          - the Base64 part of the Authorization header or None if invalid.
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None

        return authorization_header[len("Basic "):]
