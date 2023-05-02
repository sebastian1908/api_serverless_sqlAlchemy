import mysql.connector


class Conexion():
    def __init__(self):
        self.db_user = 'root'
        self.db_pass = ''
        self.db_server = 'localhost'
        self.db_name = 'apisever'

    def get_connection(self):
        cnx = mysql.connector.connect(user=self.db_user, password=self.db_pass,
                                      host=self.db_server, database=self.db_name)
        return cnx
