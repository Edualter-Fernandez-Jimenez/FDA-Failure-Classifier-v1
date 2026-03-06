import mysql.connector
from mysql.connector import Error

class DatabaseConnection:
    def __init__(self):
        """Inicializa los parámetros de configuración."""
        self.config = {
            'host': '127.0.0.1',
            'user': 'root',
            'password': '',
            'database': 'fda_code_classifier',
            'port': 3306
        }
        self._connection = None

    def connect(self):
        """Establece la conexión con la base de datos."""
        try:
            if self._connection is None or not self._connection.is_connected():
                self._connection = mysql.connector.connect(**self.config)
            return self._connection
        except Error as e:
            raise Exception(f"Error connecting to MariaDB: {e}")

    def close(self):
        """Cierra la conexión de forma segura."""
        if self._connection and self._connection.is_connected():
            self._connection.close()


    @property
    def is_alive(self):
        """Verifica si la conexión está activa."""
        return self._connection is not None and self._connection.is_connected()