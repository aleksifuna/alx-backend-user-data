#!/usr/bin/env python3
"""
Flask app configuration module
"""

from flask import Flask, jsonify, request, abort, make_response, redirect
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
    password = request.form.get('password')
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
        response = make_response(
            jsonify({
                "email": email,
                "message": "logged in"
                })
        )
        response.set_cookie('session_id', session_id)
        return response, 200
    abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """Logsout the user from the system and redirect to home
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect('/')
    abort(403)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """Checks for user then responds with details
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({
            "email": user.email
        }), 200
    abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """Generates password reset token
    """
    user_email = request.form.get('email')
    try:
        reset_token = AUTH.get_reset_password_token(user_email)
    except ValueError:
        abort(403)
    return jsonify({
        "email": user_email,
        "reset_token": reset_token
    }), 200


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password():
    """Updates the user password
    """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)
    return jsonify({
        "email": email,
        "message": "Password updated"
    }), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
