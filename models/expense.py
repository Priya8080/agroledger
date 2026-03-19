from extensions import mysql

def add_expense(user_id, expense_category, amount, expense_date, description):
    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO expenses (user_id, expense_category, amount, expense_date, description) VALUES (%s, %s, %s, %s, %s)",
        (user_id, expense_category, amount, expense_date, description)
    )
    mysql.connection.commit()
    cur.close()

def get_user_expenses(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM expenses WHERE user_id = %s ORDER BY expense_date DESC", (user_id,))
    expenses = cur.fetchall()
    cur.close()
    return expenses

def delete_expense(expense_id, user_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM expenses WHERE id = %s AND user_id = %s", (expense_id, user_id))
    mysql.connection.commit()
    cur.close()
