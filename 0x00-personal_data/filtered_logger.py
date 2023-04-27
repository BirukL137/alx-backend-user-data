#!/usr/bin/env python3
"""
Regex-ing
Log formatter
"""

import re
import logging
from typing import List


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
