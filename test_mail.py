import os
import sys
from flask import Flask
from flask_mail import Mail, Message
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

def test_smtp_settings():
    app = Flask(__name__)
    
    # Load settings from environment (matching config.py logic)
    server = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    port = int(os.environ.get('MAIL_PORT', 587))
    use_tls = os.environ.get('MAIL_USE_TLS', 'True').lower() in ['true', '1', 't']
    use_ssl = os.environ.get('MAIL_USE_SSL', 'False').lower() in ['true', '1', 't']
    username = os.environ.get('MAIL_USERNAME')
    password = os.environ.get('MAIL_PASSWORD')

    if not username or not password:
        print("ERROR: MAIL_USERNAME or MAIL_PASSWORD not found in .env file.")
        return

    app.config.update(
        MAIL_SERVER=server,
        MAIL_PORT=port,
        MAIL_USE_TLS=use_tls,
        MAIL_USE_SSL=use_ssl,
        MAIL_USERNAME=username,
        MAIL_PASSWORD=password,
        MAIL_DEFAULT_SENDER=username
    )

    mail = Mail(app)

    print(f"--- AgroLedger SMTP Diagnostics ---")
    print(f"SMTP Server: {server}:{port}")
    print(f"TLS: {use_tls}, SSL: {use_ssl}")
    print(f"Username: {username}")
    print(f"Password: {'*' * len(password) if password else 'MISSING'}")
    print(f"-----------------------------------")

    with app.app_context():
        msg = Message('AgroLedger SMTP Test',
                      recipients=[username],
                      body="If you received this, your AgroLedger email configuration is working perfectly!")
        try:
            print("Attempting to send test email...")
            mail.send(msg)
            print("\nSUCCESS: Email sent successfully!")
            print(f"Please check your inbox at {username}.")
        except Exception as e:
            print(f"\nFAILURE: {str(e)}")
            if "535" in str(e) or "BadCredentials" in str(e):
                print("\nTIP: This error usually means your password is incorrect.")
                print("If you are using Gmail, you MUST use an 'App Password':")
                print("1. Enable 2-Step Verification in your Google Account.")
                print("2. Search for 'App Passwords' in your Google Account settings.")
                print("3. Generate a new password for 'Other' and name it 'AgroLedger'.")
                print("4. Copy the 16-character code and paste it into your .env as MAIL_PASSWORD.")
            elif "ConnectionRefusedError" in str(e):
                print("\nTIP: Could not connect to the mail server. Check your MAIL_SERVER and MAIL_PORT.")

if __name__ == "__main__":
    test_smtp_settings()
