# ----------------------------------------------------------------------------------------------------------------------
from concurrent.futures import ThreadPoolExecutor
from database.ConnectionPool import *
from database.Person import Person
import json
import numpy
import cv2
import face_recognition
from controller.FaceRecognition import FaceRecognition
from threads.wrapper_pool import wrapper_pool
# ----------------------------------------------------------------------------------------------------------------------
pool = ThreadPoolExecutor(max_workers=1)


get_person_query_by_name = 'SELECT * FROM person where first_name = "{}" and last_name = "{}";'
get_person_query_by_id = 'SELECT * FROM person where id_number = "{}";'
get_person_encoding = 'SELECT * FROM person natural join encoding'
get_person_query_by_name_encoding = 'SELECT first_name, last_name, encode FROM person natural join encoding'

insert_person_query = 'INSERT INTO person (id_number, first_name, last_name, email, phone_number)\
                       VALUES("{}","{}","{}","{}","{}");'
insert_encoding_query = 'INSERT INTO encoding (id_number, encode)\
                       VALUES("{}","{}");'

create_person_table = '''CREATE TABLE IF NOT EXISTS person
  (id_number INT UNSIGNED PRIMARY KEY NOT NULL UNIQUE,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL ,
  email TEXT NOT NULL UNIQUE,
  phone_number TEXT NOT NULL UNIQUE
  );
  '''
create_encoding_table = '''CREATE TABLE IF NOT EXISTS encoding
  (
  encode TEXT NOT NULL,
  id_number INT UNSIGNED NOT NULL,
  FOREIGN KEY (id_number) REFERENCES person (id_number)
  );
  '''
# ----------------------------------------------------------------------------------------------------------------------


def insert_encoding(sfr: FaceRecognition, pool, name, id, images: [str]):

    connection = pool.get_connection()
    print("after getting connection")
    for img in images:
        image = cv2.imread (img)
        print("reading image")
        rgb_img = cv2.cvtColor (image, cv2.COLOR_BGR2RGB)
        print("before encoding")
        encoding = face_recognition.face_encodings (rgb_img, model="small")[0]
        print("after encoding")
        str_list = [str (x) for x in encoding]
        print("after str_list")
        connection.execute ('INSERT INTO encoding (id_number, encode)\
         VALUES(?,?);', (id, json.dumps (str_list)))
        print("encoded")
        sfr.append_known_face_names(name)
        sfr.append_known_face_encoding(encoding)
    connection.commit ()
    connection.close ()
    print("person added to db")


class PersonDaoImpl(object):

    # ------------------------------------------------------------------------------------------------------------------

    def __init__(self, sfr):
        self.pool = Connection_pool()
        self.connection = self.pool.get_connection()
        self.connection.execute(create_person_table)
        self.connection.execute(create_encoding_table)
        self.sfr = sfr

    # ------------------------------------------------------------------------------------------------------------------

    def get_person_by_name(self, first, last):
        cursor = self.connection.execute(get_person_query_by_name.format(str.lower(first), str.lower(last)))
        person = Person(cursor.fetchall()[0])
        return person

    # ------------------------------------------------------------------------------------------------------------------

    def get_person_by_id(self, id_num):
        cursor = self.connection.execute(get_person_query_by_id.format(id_num))
        person = Person(cursor.fetchall()[0])
        return person

    # ------------------------------------------------------------------------------------------------------------------

    def add_person(self, person,images:[str]):
        self.connection.execute (insert_person_query.format
                            (person.id_number, person.first_name, person.last_name, person.email,
                             person.phone_number))
        self.connection.commit ()
        name = person.first_name + ' ' + person.last_name

        pool.submit(insert_encoding,self.sfr, self.pool, name, person.id_number,images)


    def getPersonAndEncodings(self):
        name_encoding = []
        cursor = self.connection.execute (get_person_query_by_name_encoding)
        for row in cursor:
            name = row[0] + ' ' + row[1]
            enodes = json.loads(row[2])
            l = [numpy.float64 (x) for x in enodes]
            name_encoding.append ((name, l))
        return name_encoding

# ----------------------------------------------------------------------------------------------------------------------
