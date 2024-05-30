#!/usr/bin/env python3
"""
End-to-end intergration tests of the app
"""

import requests


def register_user(email: str, password: str) -> None:
    """Tests user registration route
    """
    data = {
        'email': email,
        'password': password
    }
    url = 'http://localhost:5000/users'

    response = requests.post(url, data=data)
    user_created = {
        'email': email,
        'message': 'user created'
    }
    assert(response.status_code == 200)
    assert(response.json() == user_created)
    response = requests.post(url, data=data)
    user_exists = {'message': 'email already registered'}
    assert(response.status_code == 400)
    assert(response.json() == user_exists)
    missing_attribute = {'message': 'Missing attribute'}
    response = requests.post(url, data={'email': email})
    assert(response.status_code == 400)
    assert(response.json() == missing_attribute)


def log_in_wrong_password(email: str, password: str) -> None:
    """Tests login route with wrong password
    """
    data = {
        'email': email,
        'password': password
    }
    url = 'http://localhost:5000/sessions'
    response = requests.post(url, data=data)
    assert(response.status_code == 401)


def log_in(email: str, password: str) -> str:
    """Tests login route with correct password"""
    data = {
        'email': email,
        'password': password
    }
    url = 'http://localhost:5000/sessions'
    response = requests.post(url, data=data)
    cookies = response.cookies
    session_id = cookies.get('session_id')
    assert(response.status_code == 200)
    return session_id


def profile_unlogged() -> None:
    """Test profile access without login
    """
    url = 'http://localhost:5000/profile'
    response = requests.get(url)
    assert(response.status_code == 403)


def profile_logged(session_id: str) -> None:
    """Test profile access with login
    """
    url = 'http://localhost:5000/profile'
    cookies = {
        'session_id': session_id
    }
    response = requests.get(url, cookies=cookies)
    assert(response.status_code == 200)
    assert(response.json())


def log_out(session_id: str) -> None:
    """Tests the logout route
    """
    url = 'http://localhost:5000/sessions'
    cookies = {
        'session_id': session_id
    }
    response = requests.delete(url, cookies=cookies)
    assert(response.status_code == 200)
    assert(response.json() == {'message': 'Bienvenue'})


def reset_password_token(email: str) -> str:
    """Tests reset password token
    """
    url = 'http://localhost:5000/reset_password'
    response = requests.post(url, data={'email': email})
    assert(response.status_code == 200)
    reset_token = response.json().get('reset_token')
    expected_json = {
        "email": email,
        "reset_token": reset_token
    }
    assert(response.json() == expected_json)
    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Tests the update password route
    """
    data = {
        'email': email,
        'reset_token': reset_token,
        'new_password': new_password
    }
    url = 'http://localhost:5000/reset_password'
    expected_json = {
        "email": email,
        "message": "Password updated"
    }
    response = requests.put(url, data=data)
    assert(response.status_code == 200)
    assert(response.json() == expected_json)


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
