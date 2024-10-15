import face_recognition
import os
import numpy as np
import cv2

class FaceRecognizer:
    def __init__(self, encodings_path):
        self.encodings_path = encodings_path
        self.known_face_encodings = []
        self.known_face_names = []
        self.load_encodings()

    def load_encodings(self):
        """Loads the known face encodings and names from the specified directory."""
        faces = os.listdir(self.encodings_path)
        images_known = [os.path.join(self.encodings_path, x) for x in faces]

        for image_path in images_known:
            known_image = face_recognition.load_image_file(image_path)
            known_face_encoding = face_recognition.face_encodings(known_image, model="large")[0]
            self.known_face_encodings.append(known_face_encoding)
            self.known_face_names.append(os.path.basename(image_path))

    def single_face_recognition(self, image_path):
        """Recognizes faces in a single image and saves the output."""
        image = face_recognition.load_image_file(image_path)
        face_locations = face_recognition.face_locations(image, model="cnn")
        print(len(face_locations), "faces found")
        
        face_encodings = face_recognition.face_encodings(image, face_locations, model="large")
        
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            name = "Unknown"
            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = self.known_face_names[best_match_index]
            
            # Draw a rectangle around the face and label it
            cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(image, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(image, os.path.splitext(name)[0], (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        output_path = "output.jpg"
        cv2.imwrite(output_path, image)
        print(f"Output saved to {output_path}")
        return output_path  # Return the path to the output image
