from sqlalchemy import create_engine

class Conexion():
    def __init__(self):
        self.db_user = 'root'
        self.db_pass = ''
        self.db_server = 'localhost'
        self.db_name = 'apisever'
        self.engine = None

    def get_connection(self):
        if not self.engine:
            connection_string = f"mysql://{self.db_user}:{self.db_pass}@{self.db_server}/{self.db_name}"
            self.engine = create_engine(connection_string)
        return self.engine.connect()
