import os

BASE_DIR = os.getcwd()

TEMPLATES_DIR = os.path.join(BASE_DIR, "app", "templates")
TEMP_UPLOAD_DIR = os.path.join(BASE_DIR, "tmp")
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")

__all__ = ("UPLOAD_DIR", "TEMP_UPLOAD_DIR", "TEMPLATES_DIR")
