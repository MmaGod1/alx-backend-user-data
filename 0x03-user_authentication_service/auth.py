#!/usr/bin/env python3
"""
Auth module to handle password hashing
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """
    Hash a password with a salt using bcrypt
    Args:
        password (str): The password to hash
    Returns:
        bytes: The salted hash of the password
    """
    salt = bcrypt.gensalt()

    # Hash the password with the salt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password
