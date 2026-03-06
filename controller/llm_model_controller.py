from typing import Optional
from network.lm_studio_service import LLMClient
import pandas as pd

class LLMModelController:
    def __init__(self, llm_client: LLMClient, db_controller):
        """
        Coordinador del modelo de lenguaje.
        :param llm_client: Instancia de nuestro cliente de red.
        :param db_controller: Instancia del controlador de BD para obtener contexto.
        """
        self.llm = llm_client
        self.db_ctrl = db_controller

    def _build_system_context(self) -> str:
        """
        Construye el string de contexto (System Prompt) basado en los datos de la BD.
        Lanza excepciones ante cualquier inconsistencia de datos para evitar alucinaciones.
        """
        try:
            # Obtenemos datos (este ya lanza su propio RuntimeError si la DB falla)
            df_context = self.db_ctrl.get_fda_annex_c()

            if df_context.empty:
                raise ValueError("El catálogo del Anexo C está vacío. No se puede proceder con la clasificación.")

            # Encabezado del Prompt
            header = (
                "### PROFILE\n"
                "You will act as a Medical Device Compliance and Classification Specialist (FDA Expert). Your accuracy is critical to patient safety.\n"
                "### TASK\n"
                "Your objective is to analyze a 'Problem Description' for a medical device and classify it using ONLY the Annex C of FDA MDR codes provided below.\n"
                "### GOLDEN RULES\n"
                "1. Do not use external knowledge. Use only the attached Annex C catalog.\n"
                "2. If the description is ambiguous, prioritize the code whose DEFINITION field is most specific.\n"
                "### REFERENCE CATALOG (APPENDIX C)\n"
            )
            header += "=" * 50 + "\n\n"

            catalog_entries = []
            for index, row in df_context.iterrows():
                # Validación estricta de integridad de datos
                fda_code = row.get('fda_cd')

                # Si falta el código FDA o la definición, la integridad del catálogo está comprometida
                if not fda_code or fda_code == "N/A" or pd.isna(fda_code):
                    raise ValueError(f"❌ Data integrity violated: Critical data is missing from the row {index} (Invalid FDA_CODE).")

                term = row.get('lvl_3_term') or row.get('lvl_2_term') or row.get('lvl_1_term') or "N/A"
                if term == "N/A":
                    raise ValueError(f"❌ Data integrity violated: No valid term was found for the code {fda_code}.")

                entry = (
                    f"TERM: {term}\n"
                    f"FDA_CODE: {fda_code}\n"
                    f"DEFINITION: {row.get('definition_desc', 'N/A')}\n"
                    f"{'-' * 30}"
                )
                catalog_entries.append(entry)

            footer = (
                "\n### OUTPUT FORMAT (STRICT)\n"
                "Returns only a JSON array with the best match. Do not add introductions or conclusions.\n"
                "Format:\n"
                "[\n {\n  'FDA_CODE': 'XXX', 'TERM': 'Term Name', 'DEFINITION': '...', \n"
                "  'PROBLEM_EXPLANATION': '...', 'CODE_EXPLANATION': '...' \n }\n]"
            )

            return header + "\n".join(catalog_entries) + footer

        except Exception as e:
            raise RuntimeError(f"❌ Error in preparing the context for the Agent: {e}")

    def process_classification(self, problem_title: str, problem_desc: str) -> str:
        """
        Orquesta la consulta al LLM (LM Studio).
        Lanza excepciones si falla la preparación del contexto o la comunicación con la IA.
        """
        try:
            sys_context = self._build_system_context()

            if not problem_title.strip() or not problem_desc.strip():
                raise ValueError("❌ The title or description of the problem cannot be empty.")

            user_prompt = f"### CASE TO ANALYZE\nTITLE: {problem_title}\nDESCRIPTION: {problem_desc}"

            result = self.llm.get_classification(sys_context, user_prompt)

            if not result:
                raise RuntimeError("❌ The AI Agent returned an empty response.")

            return result

        except ValueError as ve:
            raise ValueError(f"❌ Validation error: {ve}")
        except Exception as e:
            raise RuntimeError(f"❌ Critical error in the classification process: {e}")