from app import create_app
from extensions import mysql

app = create_app()

def migrate():
    with app.app_context():
        cur = mysql.connection.cursor()
        print("Adding otp and otp_expiry columns to users table...")
        try:
            cur.execute("ALTER TABLE users ADD COLUMN otp VARCHAR(10) DEFAULT NULL;")
            print("Successfully added otp column.")
        except Exception as e:
            print("otp column might already exist:", e)
            
        try:
            cur.execute("ALTER TABLE users ADD COLUMN otp_expiry DATETIME DEFAULT NULL;")
            print("Successfully added otp_expiry column.")
        except Exception as e:
            print("otp_expiry column might already exist:", e)
            
        cur.close()

if __name__ == '__main__':
    migrate()
