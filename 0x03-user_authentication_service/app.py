#!/usr/bin/env python3
"""
Basic Flask app
Register user
Log in
Log out
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


@app.route("DELETE /sessions")
def logout(self, request):
    """
    A method that takes a request that is expected to contain the session ID
    as a cookies. If the user exists destroy the session and redirect to GET
    '/'. Otherwise, respond with a 403 HTTP status.
    """
    session_id = request.cookies.get("session_id")
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            AUTH.destroy_session(user.id)
            return redirect("/")
    return abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
