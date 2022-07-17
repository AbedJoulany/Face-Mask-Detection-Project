# ----------------------------------------------------------------------------------------------------------------------

from database.ConnectionPool import *
from database.Person import Person
import json
import numpy
import cv2
import face_recognition
# ----------------------------------------------------------------------------------------------------------------------

get_person_query_by_name = 'SELECT * FROM perso where first_name = "{}" and last_name = "{}";'
get_person_query_by_id = 'SELECT * FROM perso where id_number = "{}";'

#insert_person_query = 'INSERT INTO person (id_number, first_name, last_name, email, phone_number)\
#                    VALUES("{}","{}","{}","{}","{}");'
insert_person_query = 'INSERT INTO perso (id_number, first_name, last_name, email, phone_number,encode)\
                       VALUES("{}","{}","{}","{}","{}","{}");'
"""create_table = '''CREATE TABLE IF NOT EXISTS person
(
  id_number INT UNSIGNED PRIMARY KEY NOT NULL UNIQUE,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL ,
  email TEXT NOT NULL UNIQUE,
  phone_number TEXT NOT NULL UNIQUE);'''"""

create_table = '''CREATE TABLE IF NOT EXISTS perso
(id_number INT UNSIGNED PRIMARY KEY NOT NULL UNIQUE,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL ,
  email TEXT NOT NULL UNIQUE,
  phone_number TEXT NOT NULL UNIQUE,
  encode TEXT NOT NULL);
  '''

# ----------------------------------------------------------------------------------------------------------------------

class PersonDaoImpl(object):

    # ------------------------------------------------------------------------------------------------------------------

    def __init__(self):
        self.pool = Connection_pool()
        self.connection = self.pool.get_connection()
        self.connection.execute(create_table)
        # self.pool.close_connection(connection)

    # ------------------------------------------------------------------------------------------------------------------

    def get_person_by_name(self, first, last):
        # connection = self.pool.get_connection()
        cursor = self.connection.execute(get_person_query_by_name.format(str.lower(first), str.lower(last)))
        person = Person(cursor.fetchall()[0])
        # self.pool.close_connection(connection)
        return person

    # ------------------------------------------------------------------------------------------------------------------

    def get_person_by_id(self, id_num):
        # connection = self.pool.get_connection()
        cursor = self.connection.execute(get_person_query_by_id.format(id_num))
        person = Person(cursor.fetchall()[0])
        # self.pool.close_connection(connection)
        return person

    # ------------------------------------------------------------------------------------------------------------------

    def add_person(self, person,images:[str]):

        encodings_str = []
        for img in images:
            image = cv2.imread (img)
            rgb_img = cv2.cvtColor (image, cv2.COLOR_BGR2RGB)
            encoding = face_recognition.face_encodings (rgb_img)[0]
            str_list = [str (x) for x in encoding]
            encodings_str.append (str_list)
        print(encodings_str)
        self.connection.execute ('INSERT INTO perso (id_number, first_name, last_name, email, phone_number,encode)\
                       VALUES(?,?,?,?,?,?);',
                      (str(person.id_number), str(person.first_name), str(person.last_name), str(person.email), str(person.phone_number),
                       json.dumps(encodings_str)))
        """self.connection.execute(insert_person_query.format(
                        person.id_number, person.first_name, person.last_name, person.email, person.phone_number,
                        json.dumps(encodings_str)))"""
        self.connection.commit()

    def getPersonAndEncodings(self):
        name_Encoding = []
        cursor = self.connection.execute ('SELECT first_name, last_name, encode FROM perso')
        for row in cursor:
            name = row[0] + ' ' + row[1]
            enodes = json.loads (row[2])
            for col in enodes:
                l = [numpy.float64 (x) for x in col]
                name_Encoding.append((name,l))
        return name_Encoding

# ----------------------------------------------------------------------------------------------------------------------
