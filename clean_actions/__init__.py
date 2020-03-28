"""Clean Actions

A Tool for generating Github Action Workflows following DRY principals.
"""

__version__ = "0.1.0"

from .api import process

__all__ = [
    "process",
]
