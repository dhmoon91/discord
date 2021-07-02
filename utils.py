"""
Utils
"""

import os

dirname = os.path.dirname(__file__)


def get_file_path(file_path):
    """Get absolute file path"""
    return os.path.join(dirname, file_path)
