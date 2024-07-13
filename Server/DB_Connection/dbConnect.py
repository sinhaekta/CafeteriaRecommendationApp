import Config
import mysql.connector
from mysql.connector import Error

class DBConnection:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DBConnection, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'connection'):
            self._connect_to_db()

    def _connect_to_db(self):
        try:
            self.connection = mysql.connector.connect(
                host = Config.DB_HOST,
                database = Config.DB_DATABASE,
                user = Config.DB_USER,
                password = Config.DB_PASSWORD
            )
            if self.connection.is_connected():
                print("Connected to MySQL database")
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")
            self.connection = None

    def get_connection(self):
        if not self.connection or not self.connection.is_connected():
            self._connect_to_db()
        return self.connection

    def close_connection(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("MySQL connection is closed")