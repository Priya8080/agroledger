from extensions import mysql

def create_user(name, email, phone, password, is_verified=True, otp=None, otp_expiry=None):
    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO users(name,email,phone,password,is_verified,otp,otp_expiry) VALUES(%s,%s,%s,%s,%s,%s,%s)",
        (name, email, phone, password, is_verified, otp, otp_expiry)
    )
    mysql.connection.commit()
    cur.close()

def update_user_password(user_id, hashed_password):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE users SET password=%s WHERE id=%s", (hashed_password, user_id))
    mysql.connection.commit()
    cur.close()

def get_user_by_email(email):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE email=%s", (email,))
    user = cur.fetchone()
    cur.close()
    return user

def get_all_unverified_users():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE is_verified=False")
    users = cur.fetchall()
    cur.close()
    return users

def verify_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE users SET is_verified=True WHERE id=%s", (user_id,))
    mysql.connection.commit()
    cur.close()

def delete_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE id=%s", (user_id,))
    mysql.connection.commit()
    cur.close()
