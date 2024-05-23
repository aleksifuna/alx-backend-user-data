#!/usr/bin/env python3
"""
Usersession module
"""

from models.base import Base


class UserSession(Base):
    """
    Class attributes and methods defination
    """

    def __init__(self, *args: list, **kwargs: dict):
        """
        Initializes the class and overloads the parent
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = self.id
