import cv2
from PyQt5.QtWidgets import QLabel, QAction, QFileDialog, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from scipy.spatial.distance import cosine

class FaceVerification:
    def __init__(self, app_window, central_widget):
        """Initialize the face verification setup."""
        self.app_window = app_window
        self.central_widget = central_widget
        self.setup_face_verification()

    def setup_face_verification(self):
        """Set up the face verification menu and layout."""
        
        menu_bar1 = self.app_window.menuBar()
        menuBarUpload = menu_bar1.addMenu("Face Comparison")

        actionLoadRefImg = QAction("Reference Image", self.app_window)
        actionLoadNewImg = QAction("New Image", self.app_window)
        actionCompareImg = QAction("Compare Images", self.app_window)

        
        menuBarUpload.addAction(actionLoadRefImg)
        menuBarUpload.addAction(actionLoadNewImg)
        menuBarUpload.addAction(actionCompareImg)
        
        actionLoadRefImg.triggered.connect(self.loadRefImg)
        actionLoadNewImg.triggered.connect(self.loadNewImg)
        actionCompareImg.triggered.connect(self.compareImages)

        self.imgRefLabel = QLabel(self.app_window)
        self.imgRefLabel.setFixedSize(250, 250)
        self.imgNewLabel = QLabel(self.app_window)
        self.imgNewLabel.setFixedSize(250, 250)

        self.resultLabel = QLabel(self.app_window)
        self.resultLabel.setAlignment(Qt.AlignCenter)
        self.resultLabel.setStyleSheet("font-size: 16px; font-weight: bold;")

        layout = QVBoxLayout(self.central_widget)
        img_layout = QHBoxLayout()
        img_layout.addWidget(self.imgRefLabel)
        img_layout.addWidget(self.imgNewLabel)

        layout.addLayout(img_layout)
        layout.addWidget(self.resultLabel)  

    def loadRefImg(self):
        """Load the reference image."""
        img_path, _= QFileDialog.getOpenFileName(self.app_window, "Select Reference Image", "", "Image Files (*.png *.jpg *.jpeg *.avif)")
        self.imgRefPath = img_path  
        self.imgRef = cv2.imread(img_path)
        self.imgRef = cv2.resize(self.imgRef, (300, 300))
        self.displayImg(self.imgRef, self.imgRefLabel)

    def loadNewImg(self):
        """Load the new image."""
        img_path, _ = QFileDialog.getOpenFileName(self.app_window, "Select New Image", "", "Image Files (*.png *.jpg *.jpeg *.avif)")
        self.imgNewPath = img_path  
        self.imgNew = cv2.imread(img_path)
        self.imgNew = cv2.resize(self.imgNew, (300, 300))
        self.displayImg(self.imgNew, self.imgNewLabel)

    def displayImg(self, image, label):
        """Display the selected image in QLabel."""
        height, width, channel = image.shape
        bytes_per_line = 3 * width
        q_image = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap.fromImage(q_image)
        
        label_width = label.width()
        label_height = label.height()
        pixmap = pixmap.scaled(label_width, label_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        label.setPixmap(pixmap)
        label.setAlignment(Qt.AlignCenter)

    def compareImages(self):
        """Compare the reference and new image using cosine similarity."""
        if not hasattr(self, 'imgRef') or not hasattr(self, 'imgNew'):
            self.resultLabel.setText("Please load both images first.")
            return

        similarity = self.compare_faces(self.imgRef, self.imgNew)
        self.resultLabel.setText(f"Similarity score: {similarity:.2f}")

        if similarity > 0.9:  
            self.resultLabel.setText("The Faces Match!")
        else:
            self.resultLabel.setText("The Faces do not match.")

    def compare_faces(self, img1, img2):
        """Compare two face images and return a similarity score."""
        img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        img1_resized = cv2.resize(img1_gray, (250, 250))
        img2_resized = cv2.resize(img2_gray, (250, 250))

    
        vector1 = img1_resized.flatten()
        vector2 = img2_resized.flatten()

        similarity = 1 - cosine(vector1, vector2)
        return similarity
