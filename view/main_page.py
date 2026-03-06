import customtkinter as ctk
from network.BD.Connection.MariaDB_Conn import DatabaseConnection
from network.BD.sql_queries import DatabaseManager
from network.lm_studio_service import LLMClient
from controller.DB_controller import DBController
from controller.llm_model_controller import LLMModelController
from view.llm_window import LLMWindow
from view.query_window import QueryWindow

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.classifier_label = "FDA FAILURE ANALYSIS"
        self.extraction_label = "SQL ADVANCED CONSOLE"

        self.title("FDA Failure Classifier")
        self.geometry("800x850")

        # 1. TECHNICAL LAYERS INITIALIZATION
        self.db_connection = DatabaseConnection()
        self.db_manager = DatabaseManager(self.db_connection)
        self.llm_client = LLMClient()

        # 2. CONTROLLERS INITIALIZATION
        self.db_ctrl = DBController(self.db_manager)
        self.llm_ctrl = LLMModelController(self.llm_client, self.db_ctrl)

        # --- TOP NAVIGATION ---
        self.nav_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.nav_frame.pack(fill="x", padx=20, pady=15)

        self.menu = ctk.CTkSegmentedButton(
            self.nav_frame,
            values=[self.classifier_label, self.extraction_label],
            command=self.navigate
        )
        self.menu.pack(fill="x")

        # --- VIEWS CONTAINER ---
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True)

        # 3. VIEWS INITIALIZATION (Injecting controllers)
        self.view_classifier = LLMWindow(self.container, self.llm_ctrl, self.db_ctrl)
        self.view_extraction = QueryWindow(self.container, self.db_ctrl)

        # Initial configuration
        self.menu.set(self.classifier_label)
        self.navigate(self.classifier_label)

    def navigate(self, selection):
        """Manages frame switching in the container."""
        self.view_classifier.pack_forget()
        self.view_extraction.pack_forget()

        if selection == self.classifier_label:
            self.view_classifier.pack(fill="both", expand=True, padx=20, pady=20)
        elif selection == self.extraction_label:
            self.view_extraction.pack(fill="both", expand=True, padx=20, pady=20)