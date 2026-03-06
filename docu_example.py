"""

Módulo de Gestión de Base de Datos para el Clasificador FDA.

Este módulo contiene la lógica principal para interactuar con MariaDB,
permitiendo ejecuciones de SQL crudo y gestión de registros de fallos.
"""

from typing import List, Dict, Any


class DatabaseManager:
    """
    Gestiona las operaciones CRUD y consultas directas a MariaDB.

    Attributes:
        db_conn (MariaDB_Conn): Instancia de la conexión activa a la base de datos.
    """

    def __init__(self, db_connection):
        self.db_conn = db_connection

    def execute_free_query(self, query: str) -> List[Dict[str, Any]]:
        """
        Ejecuta una consulta SQL personalizada (Raw SQL) de forma segura.

        Args:
            query (str): La sentencia SQL completa a ejecutar.

        Returns:
            List[Dict[str, Any]]: Una lista de diccionarios donde cada llave
                es el nombre de la columna.

        Raises:
            ValueError: Si la consulta está vacía o contiene caracteres ilegales.
            RuntimeError: Si ocurre un error de sintaxis en el motor de MariaDB.

        Example:
            >>> manager.execute_free_query("SELECT * FROM users LIMIT 1")
            [{'id': 1, 'name': 'Admin'}]
        """
        if not query.strip():
            raise ValueError("The query cannot be empty.")
        # ... lógica de ejecución ...