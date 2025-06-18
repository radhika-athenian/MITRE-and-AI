# Insert the project root into sys.path so 'services' is importable
# conftest.py
import sys
import os

# Ensure the project root (current directory) is on sys.path
ROOT = os.path.abspath(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
    
