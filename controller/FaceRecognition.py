# ----------------------------------------------------------------------------------------------------------------------

import face_recognition
import cv2
import os
import numpy as np
last_encoding = []
scale_percent = 50
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

    """def load_encoding_images(self, images_path):
        for name in os.listdir(images_path):
            print(name)
            for filename in os.listdir(f"{images_path}/{name}"):
                print(filename)
                image = cv2.imread(f"{images_path}/{name}/{filename}")
                rgb_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                encoding = face_recognition.face_encodings(rgb_img)[0]
                self.known_face_encodings.append(encoding)
                self.known_face_names.append(name)

        print("Encoding images loaded")"""

    # ------------------------------------------------------------------------------------------------------------------
    def load_encodings(self, name_encoding):
        for name, encoding in name_encoding:
            self.known_face_encodings.append(encoding)
            self.known_face_names.append(name)

    # ------------------------------------------------------------------------------------------------------------------

    def detect_known_faces(self, frame):
        # # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        name = "Unknown"
        print("1")
        width = int(frame.shape[1] * scale_percent / 100)
        height = int(frame.shape[0] * scale_percent / 100)

        # dsize
        dsize = (width, height)
        rgb_small_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        print("2")
        face_encodings = \
            face_recognition.face_encodings(rgb_small_frame, num_jitters=2, known_face_locations=[(0, frame.shape[1], frame.shape[0], 0)],
                                            model="hog")
        print("3")
        face_distances = face_recognition.face_distance(self.known_face_encodings, face_encodings[0])
        print("4")
        if face_distances.size > 0:
            print("5")
            best_match_index = np.argmin(face_distances)
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encodings[0], tolerance=0.5)
            print("6")
            if matches[best_match_index]:
                print("7")
                print(matches.count(True))
                name = self.known_face_names[best_match_index]
                if name == "Unknown":
                    return None
                """if self.countTrue(matches, self.find_indices(self.known_face_names, self.known_face_names[
                    best_match_index])) > self.known_face_names.count(self.known_face_names[best_match_index]) // 2:"""
                return name
            else:
                self.known_face_encodings.append(face_encodings[0])
                self.known_face_names.append("Unknown")
                return "Unknown"
        else:
            self.known_face_encodings.append(face_encodings[0])
            self.known_face_names.append("Unknown")
            return "Unknown"


    def find_indices(self, list_to_check, item_to_find):
        indices = []
        for idx, value in enumerate(list_to_check):
            if value == item_to_find:
                indices.append(idx)
        print(indices)
        return indices

    def countTrue(self, matches, indecies):
        count = 0
        for i in indecies:
            if matches[i]:
                count += 1
        print(count)
        return count

# ----------------------------------------------------------------------------------------------------------------------
