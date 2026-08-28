import os
import pymysql
from pymysql.cursors import DictCursor
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "flutterx")


def get_db_connection(use_db=True):
    """Establishes a connection to the MySQL server."""
    conn = pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME if use_db else None,
        autocommit=True,
        cursorclass=DictCursor
    )
    return conn


def init_db():
    """Ensures database and required tables exist on startup."""
    try:
        # First connect without database to ensure DB exists
        conn = get_db_connection(use_db=False)
        with conn.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}`;")
        conn.close()

        # Connect to DB to create tables
        conn = get_db_connection(use_db=True)
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    email VARCHAR(255) NOT NULL,
                    dob VARCHAR(50) DEFAULT NULL,
                    address TEXT DEFAULT NULL,
                    mobile_number VARCHAR(50) DEFAULT NULL
                );
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS events (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    name VARCHAR(255) NOT NULL,
                    date VARCHAR(50) NOT NULL,
                    location VARCHAR(255) NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                );
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS contributions (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    event_id INT NOT NULL,
                    amount INT NOT NULL,
                    name VARCHAR(255) DEFAULT NULL,
                    address TEXT DEFAULT NULL,
                    mobile_number VARCHAR(50) DEFAULT NULL,
                    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE
                );
            """)
        conn.close()
        print(f"Database `{DB_NAME}` and tables initialized successfully.")
    except Exception as e:
        print(f"Database initialization error: {e}")
