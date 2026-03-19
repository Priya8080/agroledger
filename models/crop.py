from extensions import mysql

def add_crop(user_id, crop_name, season, sown_date, expected_yield):
    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO crops (user_id, crop_name, season, sown_date, expected_yield) VALUES (%s, %s, %s, %s, %s)",
        (user_id, crop_name, season, sown_date, expected_yield)
    )
    mysql.connection.commit()
    cur.close()

def get_user_crops(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM crops WHERE user_id = %s", (user_id,))
    crops = cur.fetchall()
    cur.close()
    return crops

def delete_crop(crop_id, user_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM crops WHERE id = %s AND user_id = %s", (crop_id, user_id))
    mysql.connection.commit()
    cur.close()
