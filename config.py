import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
PROCESSED_FOLDER = os.path.join(BASE_DIR, 'processed')
LOG_FOLDER = os.path.join(BASE_DIR, 'logs')
SALT_FOLDER = os.path.join(BASE_DIR, 'salt')

SECRET_KEY = "your-secret-key"

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = ""
DB_NAME = "pii_hashing_system"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)
os.makedirs(LOG_FOLDER, exist_ok=True)
os.makedirs(SALT_FOLDER, exist_ok=True)