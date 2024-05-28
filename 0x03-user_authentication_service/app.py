#!/usr/bin/env python3
"""
Flask app configuration module
"""

from flask import Flask, jsonify, request, abort
from auth import Auth
app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'])
def home():
    """ Returns a json payload for home route
    """
    return jsonify({
        'message': 'Bienvenue'
    })


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """Handles user registration requests
    """
    email = request.form.get('email')
    password = request.form.get('email')
    if not email or not password:
        return jsonify({
            "message": "Missing attribute"
        }), 400
    try:
        user = AUTH.register_user(email, password)
        return jsonify({
            "email": user.email,
            "message": "user created"
        }), 200
    except ValueError:
        return jsonify({
            "message": "email already registered"
        }), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """Handles login request from users
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if not email or not password:
        abort(401)
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        return session_id
    abort(401)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
