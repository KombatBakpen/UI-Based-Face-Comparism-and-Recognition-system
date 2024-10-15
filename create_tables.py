import mysql.connector
from mysql.connector import Error


# MySQL connection details: ###constant###
mysql_config = {
    "host": "localhost",
    "user": "my_user",
    "password": "my_password",
    "port":3306
}

def main():
    db_name = "images_db"

    conn = connect_without_db()
    cursor = conn.cursor()

    create_database(cursor, db_name)
    cursor.close()
    conn.close()

    conn = connect_with_db(db_name)
    cursor = conn.cursor()

    create_table(cursor)

    conn.commit()
    cursor.close()
    conn.close()

def connect_without_db():
    return mysql.connector.connect(**mysql_config)

def connect_with_db(database_name):
    return mysql.connector.connect(database=database_name, **mysql_config)

def create_database(cursor, db_name):
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        print(f"Database '{db_name}' created or exists already.")
    except Error as e:
        print(f"Error creating database: {e}")

def create_table(cursor):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS images_store (
        id INT AUTO_INCREMENT PRIMARY KEY,
        image_name VARCHAR(255),
        image_column LONGBLOB
    );
    """
    try:
        cursor.execute(create_table_query)
        print("Table created or exists already.")
    except Error as e:
        print(f"Error creating table: {e}")


if __name__ == "__main__":
    main()
