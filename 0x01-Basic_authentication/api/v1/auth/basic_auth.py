#!/usr/bin/env python3
""" Basic Authentication Module.
"""
from .auth import Auth
import base64
from models.user import User
from typing import TypeVar


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

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> UserType:
        """Returns the User instance based on user_email and user_pwd."""       
        if not isinstance(user_email, str) or user_email is None:
            return None
        if not isinstance(user_pwd, str) or user_pwd is None:
            return None

        # Search for the user by email
        user = User.search({'email': user_email})
        if not user:
            return None
  
        user = user[0]  # if a list returns, take the first match

        # Check if the password matches
        if not user.is_valid_password(user_pwd):
            return None

        return user
