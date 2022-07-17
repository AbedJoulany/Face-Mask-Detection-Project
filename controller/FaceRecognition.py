# ----------------------------------------------------------------------------------------------------------------------

import face_recognition
import cv2
import os
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
from database.personDaoImpl import *


class FaceRecognition:

    # ------------------------------------------------------------------------------------------------------------------

    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []

        # Resize frame for a faster speed
        self.frame_resizing = 0.25

    # ------------------------------------------------------------------------------------------------------------------

    def load_encoding_images(self, images_path):
        """
        Load encoding images from path
        :param images_path:
        :return:
        """
        for name in os.listdir (images_path):
            print (name)
            for filename in os.listdir (f"{images_path}/{name}"):
                print (filename)
                image = cv2.imread (f"{images_path}/{name}/{filename}")
                rgb_img = cv2.cvtColor (image, cv2.COLOR_BGR2RGB)
                encoding = face_recognition.face_encodings (rgb_img)[0]
                self.known_face_encodings.append (encoding)
                self.known_face_names.append (name)

        print ("Encoding images loaded")

    # ------------------------------------------------------------------------------------------------------------------
    def load_encodings(self):
        """
        :return:
        """
        dao = PersonDaoImpl ()
        name_encoding = dao.getPersonAndEncodings ()
        for name, encoding in name_encoding:
            self.known_face_encodings.append (encoding)
            self.known_face_names.append (name)

    # ------------------------------------------------------------------------------------------------------------------

    def detect_known_faces(self, frame):
        # # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = cv2.cvtColor (frame, cv2.COLOR_BGR2RGB)

        face_encodings = \
            face_recognition.face_encodings (rgb_small_frame, model="small")

        face_distances = face_recognition.face_distance (self.known_face_encodings, face_encodings[0])
        name = "Unknown"

        if face_distances.size > 0:
            best_match_index = np.argmin (face_distances)
            matches = face_recognition.compare_faces (self.known_face_encodings, face_encodings[0],tolerance=0.5)
            if matches[best_match_index]:
                name = self.known_face_names[best_match_index]
        return name

# ----------------------------------------------------------------------------------------------------------------------
