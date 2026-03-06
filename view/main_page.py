"""
Main Application Entry Point for the FDA Classifier.

This module initializes the core technical layers, orchestrates dependency
injection between controllers and views, and manages top-level navigation
within the CustomTkinter graphical interface.
"""

import customtkinter as ctk
from network.BD.Connection.MariaDB_Conn import DatabaseConnection
from network.BD.sql_queries import DatabaseManager
from network.lm_studio_service import LLMClient
from controller.DB_controller import DBController
from controller.llm_model_controller import LLMModelController
from view.llm_window import LLMWindow
from view.query_window import QueryWindow

# Global UI Configuration
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class MainApp(ctk.CTk):
    """
    Root class for the FDA Failure Classifier application.

    This class serves as the 'Assembler' in the MVC pattern, initializing
    the database connection, business logic controllers, and the main
    navigation interface.

    Attributes:
        db_connection (DatabaseConnection): The primary MariaDB connection handler.
        db_manager (DatabaseManager): Handler for raw SQL and dataframe operations.
        llm_client (LLMClient): Client for local LLM inference.
        db_ctrl (DBController): Controller managing database business logic.
        llm_ctrl (LLMModelController): Controller managing LLM orchestration.
    """

    def __init__(self):
        """
        Initializes the application window, controllers, and view components.
        """
        super().__init__()

        self.classifier_label = "FDA FAILURE ANALYSIS"
        self.extraction_label = "SQL ADVANCED CONSOLE"

        self.title("FDA Failure Classifier")
        self.geometry("800x850")

        # 1. TECHNICAL LAYERS INITIALIZATION
        # These are the lowest level components of the architecture.
        self.db_connection = DatabaseConnection()
        self.db_manager = DatabaseManager(self.db_connection)
        self.llm_client = LLMClient()

        # 2. CONTROLLERS INITIALIZATION
        # Controllers receive the technical managers to act as intermediaries.
        self.db_ctrl = DBController(self.db_manager)
        self.llm_ctrl = LLMModelController(self.llm_client, self.db_ctrl)

        # --- TOP NAVIGATION ---
        # Implementation of a segmented button menu for switching between views.
        self.nav_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.nav_frame.pack(fill="x", padx=20, pady=15)

        self.menu = ctk.CTkSegmentedButton(
            self.nav_frame,
            values=[self.classifier_label, self.extraction_label],
            command=self.navigate
        )
        self.menu.pack(fill="x")

        # --- VIEWS CONTAINER ---
        # Main area where different windows (frames) are packed.
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True)

        # 3. VIEWS INITIALIZATION (Injecting controllers)
        # Views only interact with controllers, never directly with the database or LLM.
        self.view_classifier = LLMWindow(self.container, self.llm_ctrl, self.db_ctrl)
        self.view_extraction = QueryWindow(self.container, self.db_ctrl)

        # Initial view state configuration
        self.menu.set(self.classifier_label)
        self.navigate(self.classifier_label)

    def navigate(self, selection: str):
        """
        Manages the switching of frames within the main container.

        Args:
            selection (str): The label of the view to be displayed.
        """
        # Remove all views from the display
        self.view_classifier.pack_forget()
        self.view_extraction.pack_forget()

        # Pack the selected view based on the menu button pressed
        if selection == self.classifier_label:
            self.view_classifier.pack(fill="both", expand=True, padx=20, pady=20)
        elif selection == self.extraction_label:
            self.view_extraction.pack(fill="both", expand=True, padx=20, pady=20)