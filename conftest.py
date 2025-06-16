# conftest.py
import sys
import os

# Insert the project root into sys.path so 'services' is importable
PROJECT_ROOT = os.path.abspath(os.curdir)
sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, os.path.join(PROJECT_ROOT, "libs"))
os.environ.setdefault("NO_KAFKA", "1")
os.environ.setdefault("GRAPH_DB", ":memory:")