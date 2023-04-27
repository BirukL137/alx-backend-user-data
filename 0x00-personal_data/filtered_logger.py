#!/usr/bin/env python3
"""
Regex-ing
Log formatter
Create logger
Connect to secure database
"""

import re
import logging
import mysql.connector
from typing import List
from os import getenv


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    A function that returns the log message obfuscated.

    Args:
        fields (List[str]): represents all fields to obfuscate.
        redaction (str): represents by the obfuscated field.
        message (str): a string representing the log line.
        separator (str): represents the character which separates all fields
        in the log line.

    Returns:
        The log message obfuscated.
    """
    for i in fields:
        message = re.sub(i + "=.*?" + separator,
                         i + "=" + redaction + separator,
                         message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ A constructor argument fields with a list of strings type. """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        The method will filter values in incoming log records
        using filter_datum.
        """
        return filter_datum(self.fields, self.REDACTION,
                            super(RedactingFormatter, self).format(record),
                            self.SEPARATOR)


def get_logger() -> logging.Logger:
    """
    This function takes no arguments and returns a
    logging.Logger object.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    This function returns a connector to the database which is
    (mysql.connector.connection.MySQLConnection) object.
    """
    username = getenv('PERSONAL_DATA_DB_USERNAME', 'root'),
    password = getenv('PERSONAL_DATA_DB_PASSWORD', ''),
    host = getenv('PERSONAL_DATA_DB_HOST', 'localhost'),
    db = getenv('PERSONAL_DATA_DB_NAME')

    conn = mysql.connector.connection.MySQLConnection(
        user=username, password=password, host=host, database=db
    )
    return conn
