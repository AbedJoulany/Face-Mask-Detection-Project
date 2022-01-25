import cv2
from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout, QPushButton
from PyQt5.QtGui import QPixmap
import sys
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
from controller.FaceMaskDetection import *


class Video1Thread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray, QLabel)

    def __init__(self, index, img_label):
        super().__init__()
        self._run_flag = True
        self.index = index
        self.image_label = img_label

    def run(self):
        # capture from web cam
        cap1 = cv2.VideoCapture(self.index)
        print(self.index)
        while self._run_flag:
            ret1, cv_img1 = cap1.read()
            frame1 = getFrame(cv_img1)

            self.change_pixmap_signal.emit(frame1, self.image_label)
        # shut down capture system
        cap1.release()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        # self.wait()


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Face Mask Detection UI")
        self.setFixedWidth(1400)
        self.setFixedHeight(700)
        self.disply_width = 700
        self.display_height = 700
        # create the label that holds the image
        self.image_label1 = QLabel(self)
        self.image_label1.resize(self.disply_width, self.display_height)

        #self.image_label2 = QLabel(self)
        #self.image_label2.resize(self.disply_width, self.display_height)
        # create a text label
        self.startButton = QPushButton('start')
        self.startButton.clicked.connect(self.start)
        self.endButton = QPushButton('stop')
        self.endButton.clicked.connect(self.closeEvent)

        # create a vertical box layout and add the two labels
        vbox = QVBoxLayout()
        vbox.addWidget(self.image_label1)
        #vbox.addWidget(self.image_label2)
        vbox.addWidget(self.startButton)
        vbox.addWidget(self.endButton)

        # set the vbox layout as the widgets layout
        self.setLayout(vbox)

        # create the video capture thread
        self.thread1 = Video1Thread(0,self.image_label1)
        #self.thread2 = Video1Thread(1,self.image_label2)
        # connect its signal to the update_image slot
        self.thread1.change_pixmap_signal.connect(self.update_image)
        #self.thread2.change_pixmap_signal.connect(self.update_image)
        # start the thread
        # self.thread.start()

    def start(self):
        self.thread1.start()
        #self.thread2.start()

    def closeEvent(self, event):
        self.thread1.stop()
        #self.thread2.stop()
        event.accept()

    @pyqtSlot(np.ndarray,QLabel)
    def update_image(self, cv_img1, image_label):
        """Updates the image_label with a new opencv image"""
        #print("in update img")
        qt_img1 = self.convert_cv_qt(cv_img1)
        image_label.setPixmap(qt_img1)


    def convert_cv_qt(self, cv_img1):
        """Convert from an opencv image to QPixmap"""
        rgb_image1 = cv2.cvtColor(cv_img1, cv2.COLOR_BGR2RGB)

        h1, w1, ch1 = rgb_image1.shape
        bytes_per_line1 = ch1 * w1
        convert_to_Qt_format = QtGui.QImage(rgb_image1.data, w1, h1, bytes_per_line1, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    a = App()
    a.show()
    sys.exit(app.exec_())
