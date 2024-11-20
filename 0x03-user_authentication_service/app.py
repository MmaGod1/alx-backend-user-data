#!/usr/bin/env python3
"""
Flask app
"""
from flask import Flask, jsonify, request
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

    if not email or not password:
        return jsonify({"message": "email and password are required"}), 400

    try:
        # Attempt to register the user using the Auth class
        user = AUTH.register_user(email, password)
        return jsonify({
            "email": user.email,
            "message": "user created"
        }), 201
    except ValueError as err:
        # Handle the case where the email is already registered
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
