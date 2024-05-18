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


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    checks if a password is valid or not
    """
    password_bytes = password.encode('utf-8')
    if bcrypt.checkpw(password_bytes, hashed_password):
        return True
    return False
