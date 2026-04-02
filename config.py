import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-agroledger-key'
    
    # MySQL Settings (Fallback to localhost for local development)
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'mysql-7c2b22d-kumaripriya8084785476-6098.i.aivencloud.com')
    MYSQL_USER = os.environ.get('MYSQL_USER', 'avnadmin')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '') # Must be set via environment variable
    MYSQL_DB = os.environ.get('MYSQL_DB', 'defaultdb')
    MYSQL_PORT = int(os.environ.get('MYSQL_PORT', 13411))
    
    # Admin System
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'priya8080@gmail.com')

    # Flask-Mail Settings
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True').lower() in ['true', '1', 't']
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', 'False').lower() in ['true', '1', 't']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'priya8080@gmail.com') # Fallback dummy or use env
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', '') # Must be set via env var
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', MAIL_USERNAME)
