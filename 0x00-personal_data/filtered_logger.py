#!/usr/bin/env python3
"""
Module contains function filter_datum
"""
import re
from typing import List
import logging
import os
import mysql.connector
PII_FIELDS = ("name", "email", "password", "ssn", "phone")


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Constructor for the class
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        returns a reducted log message
        """
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 separator: str
                 ) -> str:
    """
    obfuscates a message and returns it
    """
    for field in fields:
        message = re.sub(f'{field}=(.*?){separator}',
                         f'{field}={redaction}{separator}', message)
    return message


def get_logger() -> logging.Logger:
    """
    Creates a Logger object and return it
    """
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False

    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = RedactingFormatter(list(PII_FIELDS))
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Creates a connector to db and return it
    """
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db = os.getenv('PERSONAL_DATA_DB_NAME')
    user = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')

    connection = mysql.connector.connect(
        host=host,
        database=db,
        user=user,
        password=password
    )

    return connection


def main() -> None:
    """
    Querries a db for and retrieves all rows in the users table
    and displays each row under a filtered format
    """
    logger = get_logger()
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    fields = ['name', 'email', 'phone', 'ssn',
              'password', 'ip', 'last_login', 'user_agent']
    for row in cursor:
        message = '; '.join(
            f'{field}={value}' for field, value in zip(fields, row)
            )
        logger.info(message)
    cursor.close()
    db.close


if __name__ == "__main__":
    main()
