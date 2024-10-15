import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from face_comparism import FaceVerification  
from faceRecognition import FaceRecognition  

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        
        self.setWindowTitle("Face App")
        self.setGeometry(100, 100, 600, 600)
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        
        self.face_verification = FaceVerification(self, central_widget)
        self.face_recognition = FaceRecognition(self, central_widget)

def main():
    """Main entry point for the application."""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
if __name__ == "__main__":
    main()
