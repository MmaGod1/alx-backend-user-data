#!/usr/bin/env python3
""" Auth module for API authentication
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Authentication class for API"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Checks if authentication is required for a given path.

        Args:
            path (str): The requested path.
            excluded_paths (List[str]):
                List of paths that are excluded from authentication
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the authorization header from the request.

        Args:
            request: The Flask request object.
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns the current user based on the request.

        Args:
            request: The Flask request object.
        """
        return None
