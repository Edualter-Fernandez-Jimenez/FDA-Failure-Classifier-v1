import pandas as pd
from typing import List, Dict, Any, Optional
from network.BD.Connection import MariaDB_Conn


class DatabaseManager:
    def __init__(self, db_connection: MariaDB_Conn):
        """
        Recibe una instancia de MariaDB_Conn para gestionar las operaciones.
        """
        self.db_conn = db_connection

    def _execute_query(self, query: str, params: Optional[tuple] = None, is_select: bool = True):
        """
        Método privado para centralizar la ejecución y manejo de errores.
        """
        conn = self.db_conn.connect()
        if not conn:
            raise ConnectionError("❌ Could not establish a connection to the database.")

        cursor = conn.cursor(dictionary=True) if is_select else conn.cursor()

        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            if is_select:
                return cursor.fetchall()
            else:
                conn.commit()
                return cursor.rowcount
        except Exception as e:
            if not is_select:
                conn.rollback()
            raise RuntimeError(f"❌ Error in SQL operation: {e}")
        finally:
            cursor.close()
            # Nota: Decidimos si cerrar la conexión aquí o dejarla abierta
            # para el siguiente proceso. Por ahora la cerramos para mantener tu lógica.
            self.db_conn.close()

    def select_data(self, table: str, columns: str = "*", where: str = None,
                    group_by: str = None, order_by: str = None) -> List[Dict[str, Any]]:
        """Construye y ejecuta una sentencia SELECT."""
        query = f"SELECT {columns} FROM {table}"
        if where: query += f" WHERE {where}"
        if group_by: query += f" GROUP BY {group_by}"
        if order_by: query += f" ORDER BY {order_by}"

        return self._execute_query(query)

    def insert_dataframe(self, table: str, df: pd.DataFrame) -> int:
        """Inserts a Pandas DataFrame in bulk with robust error handling."""
        if df.empty:
            return 0

        cols = ", ".join(df.columns)
        placeholders = ", ".join(["%s"] * len(df.columns))
        query = f"INSERT INTO {table} ({cols}) VALUES ({placeholders})"
        values = list(df.itertuples(index=False, name=None))

        # 1. Establish connection
        conn = self.db_conn.connect()
        if not conn:
            raise ConnectionError(f"❌ Could not connect to database for table: {table}")

        cursor = conn.cursor()
        try:
            # 2. Execute bulk insert
            cursor.executemany(query, values)
            conn.commit()
            return cursor.rowcount

        except Exception as e:
            # 3. CRITICAL: Rollback on failure
            conn.rollback()
            # 4. Raise the error to be caught by the Controller
            raise RuntimeError(f"❌ Bulk insert failed for table '{table}': {str(e)}") from e

        finally:
            # 5. Always clean up resources
            cursor.close()
            self.db_conn.close()

    def execute_free_query(self, query: str) -> List[Dict[str, Any]]:
        """
        Ejecuta consultas SQL personalizadas con manejo de errores robusto.
        """
        # Validación básica: evitamos que el string esté vacío
        if not query or not query.strip():
            raise ValueError("The SQL query cannot be empty.")

        try:
            # Intentamos ejecutar a través del método privado
            return self._execute_query(query, is_select=True)

        except RuntimeError as e:
            raise RuntimeError(f"❌ Critical failure while processing the query: {str(e)}")
        except Exception as e:
            raise Exception(f"❌ Execution error in Raw SQL: {e}")