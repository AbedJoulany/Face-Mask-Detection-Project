import cv2
from qt_core import *
import numpy as np
import os
from controller.simple_facerec import SimpleFacerec

FacesImagesFolder = r"savedImages/Faces"


class RecognitionThread(QThread):
    change_pixmap_signal = Signal(np.ndarray)


    def __init__(self):
        super().__init__()
        self._run_flag = True
        self.sfr = SimpleFacerec().load_encoding_images("controller/images/")

    def run(self, frame):
        face_locations, face_names = self.sfr.detect_known_faces(frame)
        for face_loc, name in zip(face_locations, face_names):
            # y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
            # cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
            # cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 4)
            facesfilename = FacesImagesFolder + "/image_" + name + ".jpg"
            cv2.imwrite(facesfilename, frame)

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()