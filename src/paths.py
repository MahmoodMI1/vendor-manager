import os
import sys


def get_root():
    """Return the project root - works both in dev and as a packaged .exe."""
    if getattr(sys, 'frozen', False):
        # Running as .exe — root is where the .exe lives
        return os.path.dirname(sys.executable)
    else:
        # Running as Python — root is one level up from src/
        return os.path.dirname(os.path.dirname(__file__))
