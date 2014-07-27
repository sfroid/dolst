"""
Methods to handle logging.

    { sfroid : 2014 }

"""

import logging
LOGGER = logging.getLogger()


def set_logging_level_to_debug():
    """
    sets loggin to debug level
    """
    LOGGER.setLevel(logging.DEBUG)


def set_logging_level_to_info():
    """
    sets loggin to debug level
    """
    LOGGER.setLevel(logging.INFO)


def set_logging_level_to_error():
    """
    sets loggin to debug level
    """
    LOGGER.setLevel(logging.ERROR)
