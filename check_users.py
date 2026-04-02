from extensions import mysql
from app import create_app

app = create_app()

with app.app_context():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, name, email, is_verified FROM users")
        users = cur.fetchall()
        print("Registered Users:")
        for user in users:
            print(f"ID: {user[0]}, Name: {user[1]}, Email: {user[2]}, Verified: {user[3]}")
        cur.close()
    except Exception as e:
        print(f"Database error: {e}")
