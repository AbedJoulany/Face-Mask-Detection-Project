# ----------------------------------------------------------------------------------------------------------------------

import face_recognition
import cv2
import os
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------

class FaceRecognition:

    # ------------------------------------------------------------------------------------------------------------------

    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []
        # Resize frame for a faster speed
        self.frame_resizing = 0.25

    # ------------------------------------------------------------------------------------------------------------------
    def append_known_face_encoding(self, encoding):
        self.known_face_encodings.append(encoding)

    def append_known_face_names(self, name):
        self.known_face_names.append(name)

    # ------------------------------------------------------------------------------------------------------------------
    def load_encodings(self, name_encoding):
        for name, encoding in name_encoding:
            self.known_face_encodings.append (encoding)
            self.known_face_names.append (name)

    # ------------------------------------------------------------------------------------------------------------------

    def detect_known_faces(self, frame):
        # # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = cv2.cvtColor (frame, cv2.COLOR_BGR2RGB)

        face_encodings = \
            face_recognition.face_encodings (rgb_small_frame, model="hog")

        face_distances = face_recognition.face_distance (self.known_face_encodings, face_encodings[0])
        name = ("Unknown", '')

        if face_distances.size > 0:
            best_match_index = np.argmin (face_distances)
            matches = face_recognition.compare_faces (self.known_face_encodings, face_encodings[0],tolerance=0.5)
            if matches[best_match_index]:
                if self.countTrue(matches, self.find_indices(self.known_face_names,
                                                             self.known_face_names[best_match_index])) >=\
                        self.known_face_names.count(self.known_face_names[best_match_index])//2:
                    name = self.known_face_names[best_match_index]
        return name

    def find_indices(self, list_to_check, item_to_find):
        indices = []
        for idx, value in enumerate (list_to_check):
            if value == item_to_find:
                indices.append(idx)
        return indices

    def countTrue(self, matches, indecies):
        count = 0
        for i in indecies:
            if matches[i]:
                count+=1
        return count

# ----------------------------------------------------------------------------------------------------------------------
