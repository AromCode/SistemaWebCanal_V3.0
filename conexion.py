import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()

class MySQLConexion:
    def __init__(self):
        self.host = os.getenv("DB_HOST")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.database = os.getenv("DB_NAME")

    def ObtenerConexion(self):
        try:
            conexion = mysql.connector.connect(
                host = self.host,
                user= self.user,
                password = self.password,
                database = self.database
            )
            if conexion.is_connected():
                return conexion
        except Error as err:
            print(f"Error....\nHubo un problema al conectarse a la base de datos...")
            return None