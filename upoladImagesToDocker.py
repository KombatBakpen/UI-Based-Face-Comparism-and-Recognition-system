import mysql.connector
from mysql.connector import Error
from PIL import Image
import io
import os

# MySQL database configuration
mysql_config = {
    "host": "localhost",
    "user": "my_user",
    "password": "my_password",
    "database": "images_db"
}

def main():
    image_paths = [
        "2.jpg",
        "3.jpg",
        "4.jpg",
        "5.jpg",
        "6.jpg"
    ]

    # Connect to the MySQL database
    conn = mysql.connector.connect(**mysql_config)
    cursor = conn.cursor()

    for image_path in image_paths:
        if os.path.exists(image_path):  
            image_name = os.path.basename(image_path)  
            image_data = read_image(image_path)  
            insert_image_to_db(cursor, image_name, image_data)
        else:
            print(f"Image '{image_path}' does not exist. Skipping...")

    # Commit the changes and close the connection
    conn.commit()
    cursor.close()
    conn.close()

def read_image(image_path):
    """Read an image and convert it to a byte array."""
    with Image.open(image_path) as img:
        img_byte_array = io.BytesIO()  # Create a BytesIO object
        img.save(img_byte_array, format=img.format)  # Save the image to the byte array
        img_byte_array = img_byte_array.getvalue()  # Get the byte data
    return img_byte_array

def insert_image_to_db(cursor, image_name, image_data):
    """Insert an image into the database."""
    try:
        cursor.execute("""
            INSERT INTO images_store (image_name, image_column) 
            VALUES (%s, %s)
        """, (image_name, image_data))  # Execute the insert command
        print(f"Image '{image_name}' inserted into the database.")
    except Error as e:
        print(f"Error inserting image '{image_name}': {e}")

if __name__ == "__main__":
    main()  # Execute the main function
