#!/usr/bin/env python3
"""
Regex-ing
"""

import re
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
