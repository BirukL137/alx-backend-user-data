#!/usr/bin/env python3
"""
Basic Flask app
Register user
"""

from flask import Flask, jsonify, request
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
