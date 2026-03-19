from extensions import mysql

def add_labour(user_id, worker_name, work_date, wages_paid):
    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO labour (user_id, worker_name, work_date, wages_paid) VALUES (%s, %s, %s, %s)",
        (user_id, worker_name, work_date, wages_paid)
    )
    mysql.connection.commit()
    cur.close()

def get_user_labour(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM labour WHERE user_id = %s ORDER BY work_date DESC", (user_id,))
    labour_logs = cur.fetchall()
    cur.close()
    return labour_logs

def delete_labour(labour_id, user_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM labour WHERE id = %s AND user_id = %s", (labour_id, user_id))
    mysql.connection.commit()
    cur.close()
