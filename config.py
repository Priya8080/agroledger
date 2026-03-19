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

