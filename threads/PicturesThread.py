import time

import cv2
from qt_core import *
import numpy as np
import os

imagesFolder = r"savedImages"


class PicturesThread (QThread):
    page_pixmap_signal = Signal (np.ndarray)
    side_pixmap_signal = Signal (np.ndarray)

    def __init__(self,q,threadLock):
        super ().__init__ ()
        self.q = q
        self._run_flag = True
        self.threadLock = threadLock

    def run(self):
        img_lst = os.listdir (imagesFolder)  # returns list
        for img in img_lst:
            print (img)
            cv_img = cv2.imread (imagesFolder + '/' + img, cv2.IMREAD_COLOR)
            self.page_pixmap_signal.emit (cv_img)
        while self._run_flag:
            if not self.q.empty():
                self.threadLock.acquire ()
                img = self.q.get()
                self.page_pixmap_signal.emit(img)
                self.side_pixmap_signal.emit(img)
                self.threadLock.release()
            time.sleep(1)

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()
