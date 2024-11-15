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
                List of paths that are excluded from authentication.

        Returns:
            True if authentication is required, False otherwise.
        """
        if path is None:
            return True
        if not excluded_paths:
            return True

        normalized_path = path.rstrip('/')

        for exc_path in excluded_paths:
            # Handle wildcard (*) at the end of the excluded path
            if exc_path.endswith('*'):
                if normalized_path.startswith(exc_path.rstrip('*')):
                    return False
            elif exc_path.rstrip('/') == normalized_path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the authorization header from the request.

        Args:
            request: The Flask request object.
        """
        if request is None:
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns the current user based on the request.

        Args:
            request: The Flask request object.
        """
        return None
