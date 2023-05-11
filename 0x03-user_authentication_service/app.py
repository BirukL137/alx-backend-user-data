#!/usr/bin/env python3
"""
Basic Flask app
Register user
Log in
Log out
user profile
Get reset password token
Update password end-point
"""

from flask import Flask, jsonify, request, abort, redirect
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/")
def index():
    """
    A method that returns a JSON payload of the form.
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users():
    """
    The /users endpoint expects two form data fields: email and password.
    If the user doesn't exists, the endpoint registers it and responds with
    JSON payload. If the user is already registered, it catches the exception
    and returns A JSON payload form with a 400 status code.
    """
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        user = AUTH.register_user(email=email, password=password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"])
def login():
    """
    A method that checks if the login information is correct and creates a
    new session for the user. If the login information is incorrect, it
    responds with a 401 HTTP status.
    """
    email = request.form.get("email")
    password = request.form.get("password")
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie("session_id", session_id)
        return response
    abort(401)


@app.route("/sessions", methods=["DELETE"])
def logout():
    """
    A method that takes a request that is expected to contain the session ID
    as a cookies. If the user exists destroy the session and redirect to GET.
    Otherwise, respond with a 403 HTTP status.
    """
    session_id = request.cookies.get("session_id")
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            AUTH.destroy_session(user.id)
            return redirect("/")
    return abort(403)


@app.route("/profile")
def profile():
    """
    A method that takes a request that is expected to contain a session ID
    cookie. If the user exists respond with a 200 HTTP status and JSON
    payload.
    """
    session_id = request.cookies.get("session_id")
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            return jsonify({"email": user.email}), 200
    abort(403)


@app.route("/reset_password", methods=["POST"])
def get_reset_password_token():
    """
    A method that takes an email request form to generate a reset password
    token when a user requests it. If the email address is not registered,
    it responds with a 403 status code. Otherwise, generate a token and
    responds with a JSON payload with 200 status code.
    """
    email = request.form.get("email")
    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token}), 200
    except ValueError:
        abort(403)


@app.route("/reset_password", methods=["PUT"])
def update_password():
    """
    A method that takes email, reset token and new password request form to
    update the password with the new one. If the token is invalid, it will
    catch an exception and responds with 403 HTTP code. Otherwise, it responds
    with a 200 HTTP code and JSON payload.
    """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")
    try:
        AUTH.update_password(reset_token=reset_token, password=new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
