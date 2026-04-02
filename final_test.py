import os
from flask import Flask
from flask_mail import Mail, Message
from dotenv import load_dotenv

# Explicitly load .env
load_dotenv()

app = Flask(__name__)
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME=os.environ.get('MAIL_USERNAME'),
    MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD'),
    MAIL_DEFAULT_SENDER=os.environ.get('MAIL_USERNAME')
)

mail = Mail(app)

print(f"Testing mail for: {app.config['MAIL_USERNAME']}")
with app.app_context():
    msg = Message('AgroLedger Final Test',
                  recipients=[app.config['MAIL_USERNAME']],
                  body="SMTP is now working!")
    try:
        mail.send(msg)
        print("RESULT: SUCCESS")
    except Exception as e:
        print(f"RESULT: FAILURE - {e}")
