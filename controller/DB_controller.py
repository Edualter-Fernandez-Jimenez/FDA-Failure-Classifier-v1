import pandas as pd
from typing import List, Dict, Any
from network.BD.sql_queries import DatabaseManager


class DBController:
    def __init__(self, db_manager: DatabaseManager):
        """
        Controlador que orquesta el flujo de datos entre la BD y la lógica de negocio.
        :param db_manager: Instancia de la clase que maneja las operaciones SQL.
        """
        self.db_manager = db_manager

    def get_fda_annex_c(self) -> pd.DataFrame:
        """
        Obtiene y limpia el contexto del Anexo C de la FDA.
        Propaga excepciones de la DB y valida la existencia de datos.
        """
        try:
            result = self.db_manager.select_data(table="fda_annex_c")

            if not result:
                raise ValueError("❌ No records were found in the table 'fda_annex_c'.")

            df = pd.DataFrame(result).fillna("")
            return df

        except Exception as e:
            # 'from e' preserva el traceback original de la conexión/query
            raise Exception(f"❌ Error processing fda_annex_c in the logic layer: {e}")


    def save_ticket_responses(self, data_list: List[Dict[str, Any]]) -> int:
        """Transforma datos de la UI y los persiste en la base de datos."""
        try:
            df = pd.DataFrame(data_list)
            return self.db_manager.insert_dataframe("event_ticket_response", df)
        except Exception as e:
            raise Exception(f"❌ Error saving tickets: {e}")
            return 0

    def get_custom_query(self, sql_query: str) -> pd.DataFrame:
        """
        Ejecuta una consulta SQL cruda.
        Lanza una excepción si la consulta falla o si no retorna resultados.
        """
        try:
            result = self.db_manager.execute_free_query(sql_query)

            if not result:
                raise ValueError(f"❌ The SQL query did not return any data: {sql_query}")

            return pd.DataFrame(result).fillna("")

        except Exception as e:
            raise Exception(f"❌ Error in the execution of custom SQL: {str(e)}")