import cv2
from qt_core import *
import numpy as np
from controller.FaceMaskDetection import getFrame

class VideoThread (QThread):
    change_pixmap_signal = Signal(np.ndarray)

    def __init__(self, q , threadLock):
        super ().__init__()
        self.q = q
        self._run_flag = True
        self.threadLock = threadLock

    def run(self):
        # capture from web cam

        try :
            cap = cv2.VideoCapture(0)
            cap.set (cv2.CAP_PROP_FRAME_WIDTH, 1290)
            cap.set (cv2.CAP_PROP_FRAME_HEIGHT, 592)
            while self._run_flag:
                ret1, cv_img = cap.read()
                if ret1:
                    frameId = cap.get(1)
                    try:
                        frame = getFrame(cv_img, frameId,self.q, self.threadLock)
                    except:
                        print("exception raised")
                    self.change_pixmap_signal.emit(frame)
                else:
                    raise Exception("camera not found")
        # shut down capture system
            cap.release()
        except Exception:
            print("camera not found")


    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()
