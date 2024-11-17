#!/usr/bin/env python3
""" Handles login with session authentication """
import os
from flask import jsonify, request
from api.v1.views import app_views
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_auth_login():
    """ Handle user login and return response based on authentication """
    email = request.form.get('email')
    password = request.form.get('password')
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    # Find the User(s) based on the email
    users = User.search({"email": email})
    # If no user is found with the given email
    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    # Iterate over all users and check the password for each
    for user in users:
        if user.is_valid_password(password):
            from api.v1.app import auth
            session_id = auth.create_session(user.id)

            response = jsonify(user.to_json())
            session_name = os.getenv('SESSION_NAME', '_my_session_id')

            # Set the session cookie
            response.set_cookie(session_name, session_id)
            return response

    # If no valid password is found, return an error
    return jsonify({"error": "wrong password"}), 401


@app_views.route('/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def session_logout():
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
