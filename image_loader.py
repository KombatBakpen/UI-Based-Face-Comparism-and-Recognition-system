import cv2
import mysql.connector
import numpy as np
from PyQt5.QtWidgets import QLabel, QGridLayout, QWidget
from PyQt5.QtGui import QPixmap, QImage

# MySQL connection details
mysql_config = {
    "host": "localhost",
    "user": "my_user",
    "password": "my_password",
    "port": 3306,
    "database": "images_db"
}

class ImageLoader(QWidget):
    def __init__(self):
        super().__init__()
        self.gridLayout = QGridLayout(self)  # Create a grid layout to display images
        self.setLayout(self.gridLayout)      # Set the layout for the QWidget

    def loadDatabase(self):
        """Load images from the MySQL database and display them in a grid."""
        conn = mysql.connector.connect(**mysql_config)  # Connect to the database
        cursor = conn.cursor()
        cursor.execute("SELECT image_column FROM images_store")  # Query image data
        images = cursor.fetchall()

        
        row, col = 0, 0
        for img_blob in images[:6]:  
            img_data = np.frombuffer(img_blob[0], np.uint8)  # Convert blob to NumPy array
            img = cv2.imdecode(img_data, cv2.IMREAD_COLOR)  # Decode the image

            if img is not None:
                label = QLabel(self)  
                self.displayImg(img, label)
                self.gridLayout.addWidget(label, row, col)  # Add QLabel to the grid

                col += 1
                if col == 3:  
                    col = 0
                    row += 1

        cursor.close()
        conn.close()

    def displayImg(self, img, label):
        """Resize and display the image in QLabel."""
        img_resized = cv2.resize(img, (250, 250))  
        height, width, channel = img_resized.shape
        q_image = QImage(img_resized.data, width, height, width * 3, QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap.fromImage(q_image)
        label.setPixmap(pixmap)  
