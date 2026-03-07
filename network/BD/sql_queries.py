"""
developer: Brian Rodríguez Orozco
email: brian.rodriguez1@ulatina.net or rodriguezbrian2302@gmail.com
id: 20200110702

Database Management Module for the FDA Classifier.

This module provides high-level abstractions for interacting with MariaDB,
supporting standard CRUD operations, bulk data insertion via Pandas,
and raw SQL execution.
"""

import pandas as pd
from typing import List, Dict, Any, Optional
from network.BD.Connection import MariaDB_Conn


class DatabaseManager:
    """
    Orchestrates database operations, including query execution and data persistence.

    Attributes:
        db_conn (MariaDB_Conn): Instance of the active connection manager.
    """

    def __init__(self, db_connection: MariaDB_Conn):
        """
        Initializes the manager with a database connection instance.

        Args:
            db_connection (MariaDB_Conn): The connection object used for all operations.
        """
        self.db_conn = db_connection

    def _execute_query(self, query: str, params: Optional[tuple] = None, is_select: bool = True):
        """
        Internal method to centralize SQL execution and exception handling.

        Args:
            query (str): The SQL statement to execute.
            params (Optional[tuple]): Positional parameters for parameterized queries.
            is_select (bool): Flag to determine if the query expects a result set.

        Returns:
            Union[List[Dict[str, Any]], int]: A list of rows for SELECT queries,
                or the row count for DML (INSERT/UPDATE/DELETE) operations.

        Raises:
            ConnectionError: If the database connection cannot be established.
            RuntimeError: If the SQL engine encounters an error during execution.
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
            self.db_conn.close()

    def select_data(self, table: str, columns: str = "*", where: str = None,
                    group_by: str = None, order_by: str = None) -> List[Dict[str, Any]]:
        """
        Dynamically constructs and executes a SELECT statement.

        Args:
            table (str): The name of the target table.
            columns (str): Comma-separated list of columns. Defaults to "*".
            where (str, optional): SQL WHERE clause filter.
            group_by (str, optional): SQL GROUP BY clause.
            order_by (str, optional): SQL ORDER BY clause.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries representing the result set.
        """
        query = f"SELECT {columns} FROM {table}"
        if where: query += f" WHERE {where}"
        if group_by: query += f" GROUP BY {group_by}"
        if order_by: query += f" ORDER BY {order_by}"

        return self._execute_query(query)

    def insert_dataframe(self, table: str, df: pd.DataFrame) -> int:
        """
        Inserts a Pandas DataFrame into the database in bulk.

        Args:
            table (str): The name of the destination table.
            df (pd.DataFrame): The DataFrame containing the data to be inserted.

        Returns:
            int: The total number of rows successfully inserted.

        Raises:
            ConnectionError: If the connection to the database fails.
            RuntimeError: If the bulk insertion process fails (triggers a rollback).
        """
        if df.empty:
            return 0

        cols = ", ".join(df.columns)
        placeholders = ", ".join(["%s"] * len(df.columns))
        query = f"INSERT INTO {table} ({cols}) VALUES ({placeholders})"
        values = list(df.itertuples(index=False, name=None))

        conn = self.db_conn.connect()
        if not conn:
            raise ConnectionError(f"❌ Could not connect to database for table: {table}")

        cursor = conn.cursor()
        try:
            cursor.executemany(query, values)
            conn.commit()
            return cursor.rowcount

        except Exception as e:
            conn.rollback()
            raise RuntimeError(f"❌ Bulk insert failed for table '{table}': {str(e)}") from e

        finally:
            cursor.close()
            self.db_conn.close()

    def execute_free_query(self, query: str) -> List[Dict[str, Any]]:
        """
        Executes a custom, raw SQL query with robust error handling.

        Args:
            query (str): The raw SQL string to be executed.

        Returns:
            List[Dict[str, Any]]: The result set of the query.

        Raises:
            ValueError: If the query string is empty or invalid.
            RuntimeError: If a critical failure occurs during execution.
            Exception: For general execution errors.
        """
        if not query or not query.strip():
            raise ValueError("The SQL query cannot be empty.")

        try:
            return self._execute_query(query, is_select=True)

        except RuntimeError as e:
            raise RuntimeError(f"❌ Critical failure while processing the query: {str(e)}")
        except Exception as e:
            raise Exception(f"❌ Execution error in Raw SQL: {e}")