#!/usr/bin/env python3
"""
Module for session authentication view
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_auth_view():
    from api.v1.app import auth
    import os
    email = request.form.get('email')
    password = request.form.get('password')
    if email is None or len(email) == 0:
        return jsonify({"error": "email missing"}), 400
    if password is None or len(password) == 0:
        return jsonify({"error": "password missing"}), 400
    user_search = User.search({'email': email})
    if len(user_search) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    user = user_search[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    user_id = user.id
    cookie_name = os.getenv('SESSION_NAME')
    session_id = auth.create_session(user_id)
    user_dict_rep = jsonify(user.to_json())
    user_dict_rep.set_cookie(cookie_name, session_id)
    return user_dict_rep
