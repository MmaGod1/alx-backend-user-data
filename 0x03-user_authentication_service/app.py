#!/usr/bin/env python3
"""
Flask app
"""
from flask import (
Flask, jsonify,
request, abort,
make_response, redirect
)
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"])
def hello() -> str:
    """ Return json respomse"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def register_user():
    """
    Endpoint to register a user.
    Expects email and password in form data.
    """
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        # Attempt to register the user using the Auth class
        user = AUTH.register_user(email, password)
        return jsonify({
            "email": user.email,
            "message": "user created"
        })
    except ValueError:
        # Handle the case where the email is already registered
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login() -> str:
    """Handles user login."""
    email = request.form.get('email')
    password = request.form.get('password')

    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)
    response = make_response(jsonify({
        'email': email,
        'message': 'logged in'
    }))
    response.set_cookie('session_id', session_id)
    
    return response


@app.route('/sessions', methods=['DELETE'])
def logout():
    session_id = request.cookies.get('session_id')

    if session_id is None:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)

    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route('/profile', methods=['GET'])
def profile():
    """Responds to the GET /profile route."""
    session_id = request.cookies.get('session_id')

    if session_id is None:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)

    return jsonify({"email": user.email}), 200


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token():
    """
    Handle POST /reset_password route
    """
    email = request.form.get("email")
    if not email:
        abort(403)

    try:
        # Generate reset token
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token}), 200
    except ValueError:
        # Email not registered
        abort(403)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
