"""
developer: Brian Rodríguez Orozco
email: brian.rodriguez1@ulatina.net or rodriguezbrian2302@gmail.com
id: 20200110702

Database Connection Module for the FDA Classifier.

This module handles the lifecycle of the MariaDB connection, ensuring
stable communication between the application and the database engine.
"""

import mysql.connector
from mysql.connector import Error

class DatabaseConnection:
    """
    Manages the lifecycle and state of the MariaDB database connection.

    Attributes:
        config (dict): Dictionary containing connection parameters (host, user, etc.).
        _connection (mysql.connector.connection_cext.CMySQLConnection): The active connection object.
    """

    def __init__(self):
        """
        Initializes the configuration parameters for the database.
        """
        self.config = {
            'host': '127.0.0.1',
            'user': 'root',
            'password': '',
            'database': 'fda_code_classifier',
            'port': 3306
        }
        self._connection = None

    def connect(self):
        """
        Establishes a connection with the MariaDB database.

        Returns:
            mysql.connector.connection_cext.CMySQLConnection: The established connection instance.

        Raises:
            Exception: If the connection to the database engine fails.
        """
        try:
            if self._connection is None or not self._connection.is_connected():
                self._connection = mysql.connector.connect(**self.config)
            return self._connection
        except Error as e:
            raise Exception(f"Error connecting to MariaDB: {e}")

    def close(self):
        """
        Safely closes the active database connection.
        """
        if self._connection and self._connection.is_connected():
            self._connection.close()

    @property
    def is_alive(self):
        """
        Verifies if the database connection is currently active.

        Returns:
            bool: True if the connection exists and is connected, False otherwise.
        """
        return self._connection is not None and self._connection.is_connected()