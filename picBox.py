from qt_core import *
from database.personDaoImpl import *

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
        self.email = QLabel (self)
        self.phone_number = QLabel(self)
        self.time = QLabel (self)
        self.verticalLayout.addWidget (self.image)
        self.verticalLayout.addWidget (self.name)
        self.verticalLayout.addWidget (self.email)
        self.verticalLayout.addWidget (self.phone_number)
        # self.frame.setLayout(self.verticalLayout)

    def setImage(self, img):
        self.image.setPixmap (img)


    def set_data(self,name):
        dao = PersonDaoImpl()

        n = name.split(' ')
        person = dao.get_person_by_name(n[0],n[1])
        print (person)
        self.name.setText(name)
        self.email.setText(person.email)
        self.phone_number.setText(person.phone_number)

