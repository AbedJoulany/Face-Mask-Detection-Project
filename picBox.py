from qt_core import *


class picBox (QWidget):

    def __init__(self, *args, **kwargs):
        super ().__init__ (*args, **kwargs)
        """self.frame = QFrame(self)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.frame.setLineWidth(2)
        self.frame.setStyleSheet("background-color:red")
        self.frame.setMaximumSize (QSize (16777215, 16777215))"""
        self.verticalLayout = QVBoxLayout (self)
        self.image = QLabel (self)
        self.name = QLabel (self)
        self.name.setText ("abed")
        self.email = QLabel (self)
        self.time = QLabel (self)
        self.verticalLayout.addWidget (self.image)
        self.verticalLayout.addWidget (self.name)
        self.verticalLayout.addWidget (self.email)
        # self.frame.setLayout(self.verticalLayout)

    def setImage(self, img):
        self.image.setPixmap (img)
