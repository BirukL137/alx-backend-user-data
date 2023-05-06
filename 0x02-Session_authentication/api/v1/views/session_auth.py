#!/usr/bin/env python3
"""
New view for Session Authentication
"""

from api.v1.views import app_views
from models.user import User
from flask import jsonify, request, abort
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """
    Returns Logged in user.
    """
    email = request.form.get('email')
    if not email:
        return jsonify({"error": "email missing"}), 400

    password = request.form.get('password')
    if not password:
        return jsonify({"error": "password missing"}), 400

    try:
        users_list = User.search({'email': email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404

    if not users_list:
        return jsonify({"error": "no user found for this email"}), 404

    for users in users_list:
        if not users.is_valid_password(password):
            return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth

    users = users_list[0]
    session_id = auth.create_session(users.id)
    SESSION_NAME = getenv("SESSION_NAME")
    response = jsonify(users.to_json())
    response.set_cookie(SESSION_NAME, session_id)
    return response


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout():
    """
    Returns empty dictionary if the process is successful
    """
    from api.v1.app import auth

    if not auth.destroy_session(request):
        abort(404)

    return jsonify({}), 200
