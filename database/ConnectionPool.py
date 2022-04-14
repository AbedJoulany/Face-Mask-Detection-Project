from mysql.connector import Error
from mysql.connector import pooling


class Connection_pool():
    __instance = None

    class Connection_pool(object):
        def __new__(cls):
            if not hasattr (cls, 'instance'):
                cls.instance = super (Connection_pool, cls).__new__ (cls)
            return cls.instance

    def __init__(self):
        try:
            self.pool = pooling.MySQLConnectionPool (pool_name="py_pool",
                                                     pool_size=2,
                                                     pool_reset_session=True,
                                                     host='localhost',
                                                     database='face_mask_db',
                                                     user='root',
                                                     password='root')
        except Error as e:
            print ("Error while connecting to MySQL using Connection pool ", e)

    def get_connection(self):
        return self.pool.get_connection()

    def close_connection(self, con):
        try:
            if con.is_connected():
                con.close()
                print ("MySQL connection is closed")
        except Error as e:
            print ("Error while connecting to MySQL using Connection pool ", e)
