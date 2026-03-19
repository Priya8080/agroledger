from extensions import mysql

def add_sale(user_id, crop_id, quantity_sold, price_per_unit, sale_date):
    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO sales (user_id, crop_id, quantity_sold, price_per_unit, sale_date) VALUES (%s, %s, %s, %s, %s)",
        (user_id, crop_id, quantity_sold, price_per_unit, sale_date)
    )
    mysql.connection.commit()
    cur.close()

def get_user_sales(user_id):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT s.*, c.crop_name 
        FROM sales s
        LEFT JOIN crops c ON s.crop_id = c.id
        WHERE s.user_id = %s
        ORDER BY s.sale_date DESC
    """, (user_id,))
    sales = cur.fetchall()
    cur.close()
    return sales

def delete_sale(sale_id, user_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM sales WHERE id = %s AND user_id = %s", (sale_id, user_id))
    mysql.connection.commit()
    cur.close()
