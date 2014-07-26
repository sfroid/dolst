"""
Methods to handle logging.
"""

def init_logging():
    import logging
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
