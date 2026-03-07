"""
developer: Brian Rodríguez Orozco
email: brian.rodriguez1@ulatina.net or rodriguezbrian2302@gmail.com
id: 20200110702

Database Controller Module for the FDA Classifier.

This module acts as the orchestration layer between the raw database operations
and the business logic, handling data transformation and validation.
"""

import pandas as pd
from typing import List, Dict, Any
from network.BD.sql_queries import DatabaseManager


class DBController:
    """
    Controller that orchestrates the data flow between the database and business logic.

    Attributes:
        db_manager (DatabaseManager): Instance of the class handling low-level SQL operations.
    """

    def __init__(self, db_manager: DatabaseManager):
        """
        Initializes the DBController with a specific DatabaseManager.

        Args:
            db_manager (DatabaseManager): The manager instance for SQL operations.
        """
        self.db_manager = db_manager

    def get_fda_annex_c(self) -> pd.DataFrame:
        """
        Retrieves and cleans the context data from the FDA Annex C table.

        Propagates database exceptions and validates the existence of records.

        Returns:
            pd.DataFrame: A cleaned DataFrame containing FDA Annex C data.

        Raises:
            ValueError: If the 'fda_annex_c' table is empty.
            Exception: If an error occurs during data retrieval or processing.
        """
        try:
            result = self.db_manager.select_data(table="fda_annex_c")

            if not result:
                raise ValueError("❌ No records were found in the table 'fda_annex_c'.")

            # fillna("") ensures compatibility with downstream logic by removing NaNs
            df = pd.DataFrame(result).fillna("")
            return df

        except Exception as e:
            # 'from e' or propagation preserves the original traceback for debugging
            raise Exception(f"❌ Error processing fda_annex_c in the logic layer: {e}")

    def save_ticket_responses(self, data_list: List[Dict[str, Any]]) -> int:
        """
        Transforms user interface data and persists it into the database.

        Args:
            data_list (List[Dict[str, Any]]): A list of dictionaries representing ticket responses.

        Returns:
            int: The number of rows successfully inserted.

        Raises:
            Exception: If the insertion process fails.
        """
        try:
            df = pd.DataFrame(data_list)
            return self.db_manager.insert_dataframe("event_ticket_response", df)
        except Exception as e:
            raise Exception(f"❌ Error saving tickets: {e}")

    def get_custom_query(self, sql_query: str) -> pd.DataFrame:
        """
        Executes a raw SQL query and returns the results as a DataFrame.

        Args:
            sql_query (str): The raw SQL statement to be executed.

        Returns:
            pd.DataFrame: The result set wrapped in a Pandas DataFrame.

        Raises:
            ValueError: If the query returns no results.
            Exception: If the SQL execution fails.
        """
        try:
            result = self.db_manager.execute_free_query(sql_query)

            if not result:
                raise ValueError(f"❌ The SQL query did not return any data: {sql_query}")

            return pd.DataFrame(result).fillna("")

        except Exception as e:
            raise Exception(f"❌ Error in the execution of custom SQL: {str(e)}")