import os
import cv2
from PyQt5.QtWidgets import QLabel, QAction, QFileDialog, QGridLayout, QWidget, QMessageBox, QVBoxLayout
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from image_loader import ImageLoader  
from write_to_new_image import ConvertToSingleImage  
from faceReconAlgorithm import FaceRecognizer  

class FaceRecognition:
    def __init__(self, appWindow, centralWidget):
        """Initialize the face recognition setup."""
        self.appWindow = appWindow
        self.centralWidget = centralWidget
        self.imageLoader = ImageLoader()  
        self.result_image_path = "output.jpg"  
        self.result_label = QLabel(self.centralWidget)  
        self.result_label.setAlignment(Qt.AlignCenter)  
        self.result_label.setFixedSize(500, 400)  
        self.setupUI()

    def setupUI(self):
        """Set up the face recognition menu and layout."""
        
        menu_bar1 = self.appWindow.menuBar()
        menuBarFaceRecognition = menu_bar1.addMenu("Face Recognition")

        actionImportReferenceData = QAction("Load Reference Data", self.appWindow)
        actionPerformRecognition = QAction("Match", self.appWindow)

        menuBarFaceRecognition.addAction(actionImportReferenceData)
        menuBarFaceRecognition.addAction(actionPerformRecognition)  

        actionImportReferenceData.triggered.connect(self.importReferenceData)
        actionPerformRecognition.triggered.connect(self.performRecognition)

        layout = QVBoxLayout(self.centralWidget)  
        layout.addWidget(self.result_label)  
        self.centralWidget.setLayout(layout)  

    def importReferenceData(self):
        """Import reference data for face recognition from the database."""
        imgDatabase = self.dBaseImage() 
        if imgDatabase is not None:
            QMessageBox.information(self.appWindow, "Info", "Database loaded. Now perform recognition by matching.")
        else:
            QMessageBox.warning(self.appWindow, "Warning", "Failed to load database images.")

    def dBaseImage(self):
        """Function to extract the combined image from the database."""
        converter = ConvertToSingleImage()  
        imgDatabase = converter.loadDatabase() 
        return imgDatabase

    def performRecognition(self):
        """Perform face recognition on loaded images."""
        encodings_directory = "Faces"  
        image_to_recognize = "dbase.jpg"  
        self.result_image_path = self.dB(encodings_directory, image_to_recognize)

        if self.result_image_path:
            self.displayOutputImage(self.result_image_path)  
        else:
            QMessageBox.warning(self.appWindow, "Warning", "Face recognition failed.")

    def dB(self, encodings_path, image_path):
        """Function to recognize faces in the specified image using the provided encodings directory."""
        face_recognizer = FaceRecognizer(encodings_path)  
        output_image_path = "output.jpg"  
        face_recognizer.single_face_recognition(image_path)  
        return output_image_path  

    def displayOutputImage(self, image_file):
        """Display the specified output image in the QLabel on the UI."""
        output_image = cv2.imread(image_file)
        if output_image is not None:
            output_image_rgb = cv2.cvtColor(output_image, cv2.COLOR_BGR2RGB)
            height, width, channel = output_image_rgb.shape
            bytes_per_line = 3 * width
            q_image = QImage(output_image_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888)
            self.result_label.setPixmap(QPixmap.fromImage(q_image))
            self.result_label.setScaledContents(True)  
            self.result_label.repaint()  
        else:
            QMessageBox.warning(self.appWindow, "Warning", "Failed to load the output image.")
        

    def displayRecognitionResult(self):
        """Display the recognition result image from the last recognition process."""
        if os.path.exists(self.result_image_path):
            self.displayOutputImage(self.result_image_path) 
        else:
            QMessageBox.information(self.appWindow, "Info", "No recognition result available to display.")
