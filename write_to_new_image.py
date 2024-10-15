import cv2
import mysql.connector
import numpy as np

"""1. MySQL connection"""
mysql_config = {
    "host": "localhost",
    "user": "my_user",
    "password": "my_password",
    "port": 3306,
    "database": "images_db"
}

"""2. Main class"""
class ConvertToSingleImage:
    def __init__(self):
        self.canvas = None
   
    def loadDatabase(self):
        """Load images from the MySQL database and return them combined into a single image."""
        conn = mysql.connector.connect(**mysql_config)  
        cursor = conn.cursor()
        cursor.execute("SELECT image_column FROM images_store")  
        images = cursor.fetchall()
        canvas_width, canvas_height = 333 * 3, 333 * 2  
        self.canvas = np.zeros((canvas_height, canvas_width, 3), dtype=np.uint8)  
        
        row, col = 0, 0
        for img_blob in images[:6]:  
            img_data = np.frombuffer(img_blob[0], np.uint8)  
            img = cv2.imdecode(img_data, cv2.IMREAD_COLOR)  

            if img is not None:
                img_resized = cv2.resize(img, (333, 333))  

                start_y = row * 333  
                start_x = col * 333  
                self.canvas[start_y:start_y + 333, start_x:start_x + 333] = img_resized  

                col += 1
                if col == 3:  
                    col = 0
                    row += 1
        cv2.imwrite("dbase.jpg", self.canvas)
        print("Image grid saved as 'dbase.jpg'")

        cursor.close()
        conn.close()
        return self.canvas  

