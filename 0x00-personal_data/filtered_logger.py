#!/usr/bin/env python3
"""
Regex-ing
"""

import re


def filter_datum(fields, redaction, message, separator):
    """
    A function that returns the log message obfuscated.

    Args:
      fields list(str): representing all fields to obfuscate.
      redaction (str): representing by what the field will be obfuscated.
      message (str): representing the log line.
      separator (str): a character separating all fields in the log line.

    Returns:
      the log message obfuscated.
    """
    for i in fields:
        message = re.sub(i + "=.*?" + separator,
                         i + "=" + redaction + separator,
                         message)
    return message
