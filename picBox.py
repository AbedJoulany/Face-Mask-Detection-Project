from qt_core import *
from database.personDaoImpl import *

class picBox (QWidget):

    def __init__(self, *args, **kwargs):
        super ().__init__ (*args, **kwargs)
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
        self.name.setText(name)
        self.email.setText(person.email)
        self.phone_number.setText(person.phone_number)

