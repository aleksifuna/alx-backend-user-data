#!/usr/bin/env python3
"""
Module supplies authentication methods
"""

import bcrypt


def _hash_password(password: str) -> bytes:
    """Hashes a password string and return bytes representation
    """
    byte_pw = password.encode('utf-8')
    hashed_pw = bcrypt.hashpw(byte_pw, bcrypt.gensalt())
    return hashed_pw
