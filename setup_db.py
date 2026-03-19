import MySQLdb

try:
    # Connect without specifying a database first
    db = MySQLdb.connect(
        host="localhost",
        user="root",
        passwd="Weirdo@09",
        port=3306
    )
    cursor = db.cursor()
    
    # Create database if not exists
    cursor.execute("CREATE DATABASE IF NOT EXISTS agroledger")
    
    # Connect to the created database
    db.select_db("agroledger")
    
    # Create users table if not exists
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL UNIQUE,
        phone VARCHAR(20) NOT NULL,
        password VARCHAR(255) NOT NULL
    )
    """)
    
    db.commit()
    print("Database and 'users' table setup successfully.")

except Exception as e:
    print(f"Error setting up database: {e}")
finally:
    if 'db' in locals():
        db.close()
