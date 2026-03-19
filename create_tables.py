import os
import pymysql
from dotenv import load_dotenv

load_dotenv()

host = os.environ.get('MYSQL_HOST', '')
user = os.environ.get('MYSQL_USER', '')
password = os.environ.get('MYSQL_PASSWORD', '')
db_name = os.environ.get('MYSQL_DB', 'defaultdb')
port = int(os.environ.get('MYSQL_PORT', 13411))

connection = pymysql.connect(
    host=host,
    user=user,
    password=password,
    db=db_name,
    port=port,
    autocommit=True,
    ssl={}
)

cursor = connection.cursor()

tables = [
    """
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        phone VARCHAR(20) NOT NULL,
        password VARCHAR(255) NOT NULL,
        is_verified BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS land (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        area DECIMAL(10,2),
        location VARCHAR(255),
        soil_type VARCHAR(100),
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS crops (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        crop_name VARCHAR(100),
        season VARCHAR(50),
        sown_date DATE,
        expected_yield DECIMAL(10,2),
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS labour (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        worker_name VARCHAR(100),
        work_date DATE,
        wages_paid DECIMAL(10,2),
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS expenses (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        expense_category VARCHAR(100),
        amount DECIMAL(10,2),
        expense_date DATE,
        description TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS sales (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        crop_id INT,
        quantity_sold DECIMAL(10,2),
        price_per_unit DECIMAL(10,2),
        sale_date DATE,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (crop_id) REFERENCES crops(id) ON DELETE SET NULL
    );
    """
]

for query in tables:
    print(f"Executing: {query.strip().splitlines()[0]}")
    cursor.execute(query)

print("Tables created successfully.")
connection.close()
