#!/usr/bin/env python3
""" Basic Authentication Module.
"""
from .auth import Auth
import base64


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
