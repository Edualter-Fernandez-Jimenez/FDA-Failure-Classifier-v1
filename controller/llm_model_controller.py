"""
developer: Brian Rodríguez Orozco
email: brian.rodriguez1@ulatina.net or rodriguezbrian2302@gmail.com
id: 20200110702

LLM Model Controller Module for the FDA Classifier.

This module coordinates the interaction between the database context and
the Language Model, ensuring that classifications are grounded in the
official FDA Annex C catalog.
"""

from network.lm_studio_service import LLMClient
import pandas as pd

class LLMModelController:
    """
    Coordinator for the Language Model operations and prompt engineering.

    Attributes:
        llm (LLMClient): Instance of the network client for LLM communication.
        db_ctrl (DBController): Instance of the database controller for context retrieval.
    """

    def __init__(self, llm_client: LLMClient, db_controller):
        """
        Initializes the controller with an LLM client and a database controller.

        Args:
            llm_client (LLMClient): The network client instance.
            db_controller (DBController): The DB controller instance to fetch context.
        """
        self.llm = llm_client
        self.db_ctrl = db_controller

    def _build_system_context(self) -> str:
        """
        Constructs the System Prompt based on Annex C data from the database.

        This method implements strict data integrity checks to prevent LLM
        hallucinations by ensuring the reference catalog is complete and valid.

        Returns:
            str: The fully formatted system context including the reference catalog.

        Raises:
            ValueError: If the catalog is empty or contains corrupted records.
            RuntimeError: If an error occurs during data retrieval or formatting.
        """
        try:
            # Fetch data (propagates RuntimeError if DB fails)
            df_context = self.db_ctrl.get_fda_annex_c()

            if df_context.empty:
                raise ValueError("The Annex C catalog is empty. Classification cannot proceed.")

            # Prompt Header
            header = ("### PROFILE\n"
                   "You will act as a Medical Device Compliance and Classification Specialist (FDA Expert). Your accuracy is critical to patient safety.\n"
                   "### TASK\n"
                   "Your objective is to analyze a 'Problem Description' for a medical device and classify it using ONLY the Annex C of FDA MDR codes provided below.\n"
                   "### GOLDEN RULES\n1. Do not use external knowledge. Use only the attached Annex C catalog.\n"
                   "2. If the description is ambiguous, prioritize the code whose\n"
                   "DEFINITION"
                   "\nfield is most specific regarding the technical failure.\n"
                   "### REFERENCE CATALOG (APPENDIX C)\n"
            )
            header += "=" * 50 + "\n\n"

            catalog_entries = []
            for index, row in df_context.iterrows():
                # Strict validation of data integrity
                fda_code = row.get('fda_cd')

                # If FDA code or definition is missing, catalog integrity is compromised
                if not fda_code or fda_code == "N/A" or pd.isna(fda_code):
                    raise ValueError(f"❌ Data integrity violated: Critical data missing at row {index} (Invalid FDA_CODE).")

                term = row.get('lvl_3_term') or row.get('lvl_2_term') or row.get('lvl_1_term') or "N/A"
                if term == "N/A":
                    raise ValueError(f"❌ Data integrity violated: No valid term found for code {fda_code}.")

                entry = (
                    f"TERM: {term}\n"
                    f"FDA_CODE: {fda_code}\n"
                    f"DEFINITION: {row.get('definition_desc', 'N/A')}\n"
                    f"{'-' * 30}"
                )
                catalog_entries.append(entry)

            footer = (
                "### OUTPUT FORMAT (STRICT)\n"
                    "Returns only a JSON array with the best match. Do not add introductions or conclusions.\n"
                    "Format:\n"
                    "[\n"
                    "{\n"
                    "'FDA_CODE': 'XXX',\n"
                    "'TERM': 'Term Name',\n"
                    "'DEFINITION': 'Original Definition',\n"
                    "'PROBLEM_EXPLANATION': 'Brief summary of why this problem fits here',\n"
                    "'CODE_EXPLANATION': 'Technical justification for the code choice'\n"
                    "}\n"
                    "]"
            )

            return header + "\n".join(catalog_entries) + footer

        except Exception as e:
            raise RuntimeError(f"❌ Error in preparing the context for the Agent: {e}")

    def process_classification(self, problem_title: str, problem_desc: str) -> str:
        """
        Orchestrates the classification request to the LLM (LM Studio).

        Args:
            problem_title (str): Short title or summary of the medical device issue.
            problem_desc (str): Detailed description of the technical problem.

        Returns:
            str: The JSON-formatted classification result from the AI.

        Raises:
            ValueError: If input fields are empty or invalid.
            RuntimeError: If the AI returns an empty response or communication fails.
        """
        try:
            sys_context = self._build_system_context()

            if not problem_title.strip() or not problem_desc.strip():
                raise ValueError("❌ The title or description of the problem cannot be empty.")

            user_prompt = f"{problem_title}\n{problem_desc}"

            result = self.llm.get_classification(sys_context, user_prompt)

            if not result:
                raise RuntimeError("❌ The AI Agent returned an empty response.")

            return result

        except ValueError as ve:
            raise ValueError(f"❌ Validation error: {ve}")
        except Exception as e:
            raise RuntimeError(f"❌ Critical error in the classification process: {e}")