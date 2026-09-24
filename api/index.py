"""Vercel serverless entrypoint.

Vercel looks for the WSGI callable `app` inside files under `api/`.
We simply re-export the real Flask app from `web/app.py`.
"""
import sys
import os

# Make sure `web/` is importable so `from app import app` works
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEB_DIR = os.path.join(ROOT, "web")
sys.path.insert(0, WEB_DIR)
sys.path.insert(0, ROOT)

# Re-export the Flask app for Vercel
from app import app  # noqa: E402,F401