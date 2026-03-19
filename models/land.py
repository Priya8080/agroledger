from extensions import mysql

def add_land(user_id, area, location, soil_type):
    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO land (user_id, area, location, soil_type) VALUES (%s, %s, %s, %s)",
        (user_id, area, location, soil_type)
    )
    mysql.connection.commit()
    cur.close()

def get_user_lands(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM land WHERE user_id = %s", (user_id,))
    lands = cur.fetchall()
    cur.close()
    return lands

def delete_land(land_id, user_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM land WHERE id = %s AND user_id = %s", (land_id, user_id))
    mysql.connection.commit()
    cur.close()
