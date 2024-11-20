#!/usr/bin/env python3
"""
Main file
"""
import requests

BASE_URL = "http://localhost:5000"


def register_user(email: str, password: str) -> None:
    """
    Registers a user by sending a POST request to /sessions with the user's
    email and password. Asserts that the registration is successful.

    Arguments:
        email (str): The user's email address.
        password (str): The user's password.
    """
    data = {"email": email, "password": password}
    response = requests.post(f"{BASE_URL}/sessions", data=data)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "logged in"}


def log_in_wrong_password(email: str, password: str) -> None:
    """
    Attempts to log in with a wrong password by
    sending a POST request to /sessions.
    Asserts that the response status is 403 (Forbidden) since the
    password is incorrect.

    Arguments:
        email (str): The user's email address.
        password (str): The incorrect password.
    """
    data = {"email": email, "password": password}
    response = requests.post(f"{BASE_URL}/sessions", data=data)
    assert response.status_code == 403


def log_in(email: str, password: str) -> str:
    """
    Login user by sending a POST request to /sessions with email
    and password. Returns the session ID from the cookies if successful login.

    Arguments:
        email (str): The user's email address.
        password (str): The correct password.

    Returns:
        str: The session ID returned in the cookies.
    """
    data = {"email": email, "password": password}
    response = requests.post(f"{BASE_URL}/sessions", data=data)
    assert response.status_code == 200
    assert "session_id" in response.cookies
    return response.cookies["session_id"]


def profile_unlogged() -> None:
    """
    Attempts to access the profile page without being logged in.
    Expects a 403 Forbidden response since no valid session is provided.
    """
    response = requests.get(f"{BASE_URL}/profile")
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """
    Access the profile page while logged in by sending a GET request
    with a valid session ID in the cookies.

    Arguments:
        session_id (str): The valid session ID from a logged-in user.
    """
    cookies = {"session_id": session_id}
    response = requests.get(f"{BASE_URL}/profile", cookies=cookies)
    assert response.status_code == 200
    assert "email" in response.json()


def log_out(session_id: str) -> None:
    """
    Logs out the user by sending a DELETE request to /sessions with
    the session ID. Expects the session to be deleted, resulting
    in no session_id in the response cookies.

    Arguments:
        session_id (str): The valid session ID for the user.
    """
    cookies = {"session_id": session_id}
    response = requests.delete(f"{BASE_URL}/sessions", cookies=cookies)
    assert response.status_code == 200
    assert "session_id" not in response.cookies


def reset_password_token(email: str) -> str:
    """
    Requests a password reset token by sending a POST request to
    /reset_password with the user's email.
    Returns the reset token if the email is valid.

    Arguments:
        email (str): The user's email address.

    Returns:
        str: The reset token generated for the user.
    """
    data = {"email": email}
    response = requests.post(f"{BASE_URL}/reset_password", data=data)
    assert response.status_code == 200
    assert "reset_token" in response.json()
    return response.json()["reset_token"]


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    Updates the user's password by sending a PUT request to /reset_password
    with the user's email, reset token, and new password.
    Verifies that the password is updated.

    Arguments:
        email (str): The user's email address.
        reset_token (str):
            the reset token provided during the password reset request.
        new_password (str): The new password to set for the user.
    """
    data = {"email": email, "reset_token": reset_token, "new_password": new_password}
    response = requests.put(f"{BASE_URL}/reset_password", data=data)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "Password updated"}


# Main execution block
EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"

if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
