import face_recognition
import cv2
import os
import glob
import numpy as np


class SimpleFacerec:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []

        # Resize frame for a faster speed
        self.frame_resizing = 0.25

    def load_encoding_images(self, images_path):
        """
        Load encoding images from path
        :param images_path:
        :return:
        """
        for name in os.listdir(images_path):
            print(name)
            for filename in os.listdir(f"{images_path}/{name}"):
                print(filename)
                image = cv2.imread(f"{images_path}/{name}/{filename}")
                rgb_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                encoding = face_recognition.face_encodings(rgb_img)[0]
                self.known_face_encodings.append(encoding)
                self.known_face_names.append(name)

        print("Encoding images loaded")

    def detect_known_faces(self, frame):

        # # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        face_encodings = face_recognition.face_encodings(rgb_small_frame)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            name = "Unknown"

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            print(face_distances)
            if face_distances.size > 0:
                best_match_index = np.argmin(face_distances)
                print(best_match_index)
                if matches[best_match_index]:
                    name = self.known_face_names[best_match_index]
            face_names.append(name)

        return face_names
