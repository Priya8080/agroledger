import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-agroledger-key'
    
    # MySQL Settings (Fallback to localhost for local development)
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'Weirdo@09') # Local DB Password
    MYSQL_DB = os.environ.get('MYSQL_DB', 'agroledger')
    MYSQL_PORT = int(os.environ.get('MYSQL_PORT', 3306))

    # Mail Settings (for OTP)
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    # REPLACE THESE WITH YOUR GMAIL AND APP PASSWORD
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'your-email@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'your-app-password'
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_USERNAME') or 'your-email@gmail.com'
