#!/usr/bin/env python3

"""
Supplies a function hash_password
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    hashes a string using bcrypt with hashpw
    """
    password_bytes = password.encode('utf-8')
    return bcrypt.hashpw(password_bytes, bcrypt.gensalt())
