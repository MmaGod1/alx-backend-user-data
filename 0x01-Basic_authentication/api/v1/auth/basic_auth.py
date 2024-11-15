#!/usr/bin/env python3
""" Basic Authentication Module.
"""
from api.v1.auth.auth import Auth
import base64
from models.user import User
from typing import TypeVar

UserType = TypeVar('User')


class BasicAuth(Auth):
    """ Inherits fro Auth class and
    performes a Basic Authentication.
    """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        Returns:
          str - the Base64 part of the Authorization header or None if invalid.
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None

        return authorization_header[len("Basic "):]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        """ Args:
            base64_authorization_header (str): The Base64 encoded string.

        Returns:
            str - The decoded value as a UTF-8 string, or None if invalid.
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None

        try:
            # Decode the Base64 string
            decoded_bytes = base64.b64decode(base64_authorization_header)
            # Convert bytes to a UTF-8 string
            return decoded_bytes.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                 str) -> (str, str):
        """Extract user email and password from the Base64 decoded value.
        Args:
            decoded_base64_authorization_header (str):
             The Base64 decoded string.

        Returns:
            tuple: A tuple containing the user email and password,
            or (None, None) if invalid.
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)

        # Split the str into email and password at the first ':'
        user_email, pswd = decoded_base64_authorization_header.split(':', 1)
        return (user_email, pswd)

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> UserType:
        """
        Returns a User instance based on user_email and user_pwd.
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        try:
            users = User.search({"email": user_email})
            if not users:
                return None

            for user in users:
                if user.is_valid_password(user_pwd):
                    return user

            return None  # No matching password
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the User instance for a request.
        """
        # Get the Authorization header from the request
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None
        
        # Extract the Base64 part from the Authorization header
        base64_auth = self.extract_base64_authorization_header(auth_header)
        if base64_auth is None:
            return None
        
        # Decode the Base64 string
        decoded_auth = self.decode_base64_authorization_header(base64_auth)
        if decoded_auth is None:
            return None
        
        # Extract user email and pswd from the decoded string
        user_email, user_pwd = self.extract_user_credentials(decoded_auth)
        if user_email is None or user_pwd is None:
            return None
        
        # Retrieve the User object from email and pswd
        user = self.user_object_from_credentials(user_email, user_pwd)
        return user

