from database.ConnectionPool import *
from database.Person import Person
get_person_query = 'SELECT * FROM person where first_name = "{}" and last_name = "{}";'


class PersonDaoImpl(object):

    def __init__(self):
        self.pool = Connection_pool()

    def get_person_by_name(self, first, last):
        connection = self.pool.get_connection()
        cursor = connection.cursor()
        cursor.execute (get_person_query.format (first, last))
        result = cursor.fetchall()
        self.pool.close_connection(connection)
        return Person(result[0])
