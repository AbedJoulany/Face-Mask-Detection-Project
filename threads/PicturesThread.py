import time

import cv2
from qt_core import *
import numpy as np
import os

imagesFolder = r"savedImages"


class PicturesThread (QThread):
    change_pixmap_signal = Signal (np.ndarray)

    def __init__(self,q):
        super ().__init__ ()
        self.q = q
        self._run_flag = True

    def run(self):
        img_lst = os.listdir (imagesFolder)  # returns list
        for img in img_lst:
            print (img)
            cv_img = cv2.imread (imagesFolder + '/' + img, cv2.IMREAD_COLOR)
            self.change_pixmap_signal.emit (cv_img)
        while self._run_flag:
            time.sleep(1)
            if not self.q.empty():
                self.change_pixmap_signal.emit (self.q.get())

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()
