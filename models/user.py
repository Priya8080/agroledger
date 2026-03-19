from extensions import mysql

def create_user(name, email, phone, password, is_verified=False):
    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO users(name,email,phone,password,is_verified) VALUES(%s,%s,%s,%s,%s)",
        (name, email, phone, password, is_verified)
    )
    mysql.connection.commit()
    cur.close()

def get_user_by_email(email):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE email=%s", (email,))
    user = cur.fetchone()
    cur.close()
    return user
