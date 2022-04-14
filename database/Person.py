class Person:

    """def __init__(self, id_number, first_name, last_name, email, phone_number):
        self.id_number = id_number
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number"""

    def __init__(self, args):
        self.id_number = args[0]
        self.first_name = args[1]
        self.last_name = args[2]
        self.email = args[3]
        self.phone_number = args[4]

    def get_id(self):
        return self.id_number

    def set_id(self,id_number):
        self.id_number = id_number

    def get_first_name(self):
        return self.first_name

    def set_first_name(self, first_name):
        self.first_name = first_name

    def get_last_name(self):
        return self.last_name

    def set_last_name(self, last_name):
        self.last_name = last_name

    def get_email(self):
        return self.email

    def set_email(self, email):
        self.email = email

    def get_phone_number(self):
        return self.phone_number

    def set_phone_number(self, phone_number):
        self.phone_number = phone_number
