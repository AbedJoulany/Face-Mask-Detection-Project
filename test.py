"""from personDaoImpl import *


dao = PersonDaoImpl()

dao.get_person_by_name('abedallah','joulany')"""
import sqlite3
import os.path


BASE_DIR = os.path.dirname (os.path.abspath ("face_mask.db"))
db_path = os.path.join (BASE_DIR, "face_mask.db")
conn = sqlite3.connect(db_path)
print ("Opened database successfully")

"""conn.execute('''CREATE TABLE IF NOT EXISTS person
(
  id_number INT UNSIGNED PRIMARY KEY NOT NULL UNIQUE,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL ,
  email TEXT NOT NULL UNIQUE,
  phone_number TEXT NOT NULL UNIQUE);''')"""

conn.execute ('INSERT INTO person (id_number, first_name, last_name, email, phone_number)'
              ' VALUES("206461394","abedallah","joulany","abedallah99@gmail.com","0528038984");')
conn.commit()

"""cursor = conn.execute('SELECT *'
                      ' FROM person where first_name = "{}" and last_name = "{}";'.format("abedallah","joulany"))"""
for row in cursor:
    print(row)
conn.close ()
