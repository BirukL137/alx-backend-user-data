#!/usr/bin/env python3
"""
End-to-end integration test
"""

import requests


def register_user(email: str, password: str) -> None:
    """
    A test method with email and password string argument and returns 200 HTTP
    code if the response is correct.
    """
    response = requests.post("http://127.0.0.1:5000/users",
                             data={"email": email, "password": password})
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    """
    A test method with email and password string argument and returns 401 HTTP
    code if the user tries to login with a wrong password.
    """
    response = requests.post("http://127.0.0.1:5000/sessions",
                             data={"email": email, "password": password})
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """
    A test method with email and password string argument and returns 200 HTTP
    code if the user logged in with a correct email and password.
    """
    response = requests.post("http://127.0.0.1:5000/sessions",
                             data={"email": email, "password": password})
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "logged in"}
    return response.cookies.get("session_id")


def profile_unlogged() -> None:
    """
    A test method for profile_unlogged
    """
    response = requests.get("http://127.0.0.1:5000/profile")
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """
    A test method with session ID string argument and returns 200 HTTP
    code if the response is correct.
    """
    response = requests.get("http://127.0.0.1:5000/profile",
                            cookies={"session_id": session_id})
    assert response.status_code == 200
    assert response.json() == {"email": EMAIL}


def log_out(session_id: str) -> None:
    """
    A test method with session ID string argument and returns 200 HTTP
    code if the response is correct.
    """
    response = requests.delete("http://127.0.0.1:5000/sessions",
                               cookies={"session_id": session_id})
    assert response.status_code == 200


def reset_password_token(email: str) -> str:
    """
    A test method with email string argument and returns 200 HTTP
    code if the response is Ok.
    """
    response = requests.post("http://127.0.0.1:5000/reset_password",
                             data={"email": email})
    assert response.status_code == 200
    return response.json().get("reset_token")


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    A test method with email, reset token and new password string argument
    and returns 200 HTTP code if the response JSON payload get validated.
    """
    response = requests.put("http://127.0.0.1:5000/reset_password",
                            data={"email": email, "reset_token": reset_token,
                                  "new_password": new_password})
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "Password updated"}


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
