import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root"
)
cursor = conn.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS client_query_db")
cursor.execute("USE client_query_db")

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    username VARCHAR(50) PRIMARY KEY,
    hashed_password TEXT,
    role VARCHAR(10)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS queries (
    query_id INT AUTO_INCREMENT PRIMARY KEY,
    mail_id VARCHAR(100),
    mobile_number VARCHAR(15),
    query_heading TEXT,
    query_description TEXT,
    image BLOB,
    status VARCHAR(10),
    query_created_time DATETIME,
    query_closed_time DATETIME
)
""")

conn.commit()
conn.close()
