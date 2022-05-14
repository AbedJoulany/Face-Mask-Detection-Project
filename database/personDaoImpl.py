from database.ConnectionPool import *
from database.Person import Person
get_person_query_by_name = 'SELECT * FROM person where first_name = "{}" and last_name = "{}";'
get_person_query_by_id = 'SELECT * FROM person where id_number = "{}";'

insert_person_query = 'INSERT INTO person (id_number, first_name, last_name, email, phone_number)\
                    VALUES("{}","{}","{}","{}","{}");'
create_table = '''CREATE TABLE IF NOT EXISTS person
(
  id_number INT UNSIGNED PRIMARY KEY NOT NULL UNIQUE,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL ,
  email TEXT NOT NULL UNIQUE,
  phone_number TEXT NOT NULL UNIQUE);'''



class PersonDaoImpl(object):

    def __init__(self):
        self.pool = Connection_pool()
        self.connection = self.pool.get_connection()
        self.connection.execute(create_table)
        #self.pool.close_connection(connection)

    def get_person_by_name(self, first, last):
        #connection = self.pool.get_connection()
        cursor = self.connection.execute (get_person_query_by_name.format(str.lower(first), str.lower(last)))
        person = Person (cursor.fetchall()[0])
        #self.pool.close_connection(connection)
        return person

    def get_person_by_id(self, id_num):
        #connection = self.pool.get_connection()
        cursor = self.connection.execute (get_person_query_by_id.format(id_num))
        person = Person (cursor.fetchall ()[0])
        #self.pool.close_connection(connection)
        return person

    def add_person(self,person):
        #connection = self.pool.get_connection()
        self.connection.execute (insert_person_query.format(
        person.id_number,person.first_name,person.last_name,person.email,person.phone_number))
        self.connection.commit()
        #self.pool.close_connection(connection)
