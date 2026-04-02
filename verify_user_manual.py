from extensions import mysql
from app import create_app

app = create_app()

def verify_specific_user(email):
    with app.app_context():
        try:
            cur = mysql.connection.cursor()
            cur.execute("UPDATE users SET is_verified=1 WHERE email=%s", (email,))
            mysql.connection.commit()
            if cur.rowcount > 0:
                print(f"User {email} verified successfully!")
            else:
                print(f"User {email} not found in database.")
            cur.close()
        except Exception as e:
            print(f"Database error: {e}")

if __name__ == "__main__":
    verify_specific_user('priya0a23@gmail.com')
