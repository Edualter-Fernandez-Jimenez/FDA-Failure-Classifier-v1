"""
developer: Brian Rodríguez Orozco
email: brian.rodriguez1@ulatina.net or rodriguezbrian2302@gmail.com
id: 20200110702

GUI View Module for the FDA Classifier.

This module implements the user interface using CustomTkinter, providing
fields for case entry, asynchronous execution of AI analysis, and
interaction with the database controller.
"""

import customtkinter as ctk
import threading
import json
from tkinter import messagebox
from typing import List, Dict, Any

class LLMWindow(ctk.CTkFrame):
    """
    Main UI frame for FDA Failure Analysis and classification.

    Attributes:
        llm_ctrl (LLMModelController): Controller for AI logic.
        db_ctrl (DBController): Controller for database interactions.
        last_result (List[Dict[str, Any]]): Storage for the most recent classification data.
    """

    def __init__(self, master, llm_controller, db_controller, **kwargs):
        """
        Initializes the UI components and sets up placeholders.

        Args:
            master: The parent widget.
            llm_controller (LLMModelController): Orchestrator for the LLM.
            db_controller (DBController): Data access orchestrator.
        """
        super().__init__(master, **kwargs)

        self.llm_ctrl = llm_controller
        self.db_ctrl = db_controller
        self.last_result: List[Dict[str, Any]] = []

        # Placeholder Configuration
        self.placeholders = {
            "entry1": "Describe the technical problem here...",
            "entry2": "Add additional context or investigation results..."
        }
        self.color_placeholder = "gray"
        self.color_normal = ("black", "white")

        self._setup_ui()

    def _setup_ui(self):
        """
        Builds the layout of the window, including inputs and action buttons.
        """
        self.lb_title = ctk.CTkLabel(self, text="FDA FAILURE ANALYSIS", font=ctk.CTkFont(size=20, weight="bold"))
        self.lb_title.pack(pady=(20, 10))

        # Case Code
        self.lb_case = ctk.CTkLabel(self, text="Case Code:", anchor="w")
        self.lb_case.pack(fill="x", padx=20, pady=(5, 0))
        self.entry_case = ctk.CTkEntry(self, placeholder_text="e.g. EVT-0001")
        self.entry_case.pack(fill="x", padx=20, pady=(0, 10))

        # Text Inputs
        self.entry1 = self._create_input_section("Problem Description (Input 1):", self.placeholders["entry1"])
        self.entry2 = self._create_input_section("Additional Context (Input 2):", self.placeholders["entry2"])

        # Output Textbox
        self.lb_output = ctk.CTkLabel(self, text="Analysis Result:", anchor="w")
        self.lb_output.pack(fill="x", padx=20, pady=(10, 0))
        self.tb_output = ctk.CTkTextbox(self, height=120, state="disabled")
        self.tb_output.pack(fill="both", padx=20, pady=(5, 15), expand=True)

        self._create_buttons()

    def _create_input_section(self, title: str, placeholder: str) -> ctk.CTkTextbox:
        """
        Creates a labeled text input section with placeholder behavior.

        Args:
            title (str): The label text for the section.
            placeholder (str): The ghost text to show when empty.

        Returns:
            ctk.CTkTextbox: The configured textbox instance.
        """
        label = ctk.CTkLabel(self, text=title, anchor="w")
        label.pack(fill="x", padx=20, pady=(10, 0))

        textbox = ctk.CTkTextbox(self, height=70, text_color=self.color_placeholder)
        textbox.insert("1.0", placeholder)
        textbox.pack(fill="x", padx=20, pady=(5, 10))

        textbox.bind("<FocusIn>", lambda e: self._handle_placeholder(textbox, placeholder, "in"))
        textbox.bind("<FocusOut>", lambda e: self._handle_placeholder(textbox, placeholder, "out"))
        return textbox

    def _handle_placeholder(self, textbox: ctk.CTkTextbox, placeholder: str, mode: str):
        """
        Manages focus events to show/hide placeholder text.

        Args:
            textbox (ctk.CTkTextbox): The target textbox.
            placeholder (str): The text to toggle.
            mode (str): Either "in" (focus gained) or "out" (focus lost).
        """
        current_text = textbox.get("1.0", "end-1c").strip()
        if mode == "in":
            if current_text == placeholder:
                textbox.delete("1.0", "end")
                textbox.configure(text_color=self.color_normal)
        elif mode == "out":
            if not current_text:
                textbox.insert("1.0", placeholder)
                textbox.configure(text_color=self.color_placeholder)

    def _create_buttons(self):
        """
        Initializes the action buttons for cleaning, executing, and saving data.
        """
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(fill="x", padx=20, pady=10)

        self.btn_clean = ctk.CTkButton(self.button_frame, text="Clean", fg_color="#4a4a4a",
                                       command=self.clean_fields)
        self.btn_clean.pack(side="left", padx=(0, 10))

        self.btn_execute = ctk.CTkButton(self.button_frame, text="Execute Analysis", fg_color="#2ecc71",
                                         command=self.run_analysis)
        self.btn_execute.pack(side="right", padx=(10, 0))

        self.btn_save = ctk.CTkButton(self.button_frame, text="Save to DB", command=self.save_data)
        self.btn_save.pack(side="right")

    def run_analysis(self):
        """
        Validates UI inputs and launches the AI analysis in a background thread.
        """
        case_code = self.entry_case.get().strip()
        text1 = self.entry1.get("1.0", "end-1c").strip()
        text2 = self.entry2.get("1.0", "end-1c").strip()

        # UI Validation
        is_empty1 = (text1 == "" or text1 == self.placeholders["entry1"])
        is_empty2 = (text2 == "" or text2 == self.placeholders["entry2"])

        if not case_code or is_empty1 or is_empty2:
            messagebox.showwarning("Empty Fields", "⚠️ Please complete all required fields.")
            return

        self._set_ui_state("disabled")
        self.refresh_output("🤖 Processing Case... Please wait.")

        threading.Thread(
            target=self._run_analysis_thread,
            args=(case_code, text1, text2),
            daemon=True
        ).start()

    def _run_analysis_thread(self, case_code: str, text1: str, text2: str):
        """
        Background thread worker for LLM processing to prevent UI freezing.

        Args:
            case_code (str): The unique identifier for the case.
            text1 (str): Primary problem description.
            text2 (str): Secondary investigation context.
        """
        try:
            # 1. Orchestrator call
            raw_result = self.llm_ctrl.process_classification(text1, text2)

            # 2. JSON Parsing attempt
            try:
                data = json.loads(raw_result)

            except json.JSONDecodeError:
                raise RuntimeError("The AI responded with an invalid format (Non-JSON).")

            # 3. Success: Process and display
            self._process_and_display(data, case_code, text1, text2)

        except ValueError as ve:
            msg = str(ve)
            self.after(0, lambda: self.refresh_output("⚠️ Analysis stopped due to validation."))
            self.after(0, lambda: messagebox.showwarning("Data Inconsistency", f"⚠️ {msg}"))

        except Exception as e:
            msg = str(e)
            self.after(0, lambda: self.refresh_output("❌ Critical error during analysis."))
            self.after(0, lambda: messagebox.showerror("System Failure", f"An error has occurred:\n\n{msg}"))

        finally:
            self.after(0, lambda: self._set_ui_state("normal"))

    def _process_and_display(self, data: List[Dict], case_code: str, text1: str, text2: str):
        """
        Maps AI response keys to database columns and updates the UI output.

        Args:
            data (List[Dict]): The raw parsed JSON list from the AI.
            case_code (str): The case identifier.
            text1 (str): Original input 1.
            text2 (str): Original input 2.
        """
        mapping = {
            "FDA_CODE": "ia_fda_cd",
            "TERM": "ia_fda_term_desc",
            "DEFINITION": "ia_fda_deff_desc",
            "PROBLEM_EXPLANATION": "ia_problem_explanation_desc",
            "CODE_EXPLANATION": "ia_code_explanation_desc"
        }

        self.last_result = []
        display_text = ""

        for item in data:
            new_item = {mapping.get(k, k): v for k, v in item.items()}
            new_item.update({
                "case_cd": case_code,
                "event_summary_desc": text1,
                "investigation_desc": text2
            })
            self.last_result.append(new_item)

            display_text += (f"CODE: {new_item.get('ia_fda_cd', '').capitalize()}\n"
                             f"TERM: {new_item.get('ia_fda_term_desc', '').capitalize()}\n"
                             f"DEFINITION: {new_item.get('ia_fda_deff_desc', '').capitalize()}\n"
                             f"PROBLEM_EXPLANATION: {new_item.get('ia_problem_explanation_desc', '').capitalize()}\n"
                             f"CODE_EXPLANATION: {new_item.get('ia_code_explanation_desc', '').capitalize()}\n"
                             f"{'-' * 40}\n")

        self.after(0, lambda: self.refresh_output(display_text))

    def save_data(self):
        """
        Persists the current analysis result into the database.
        """
        if not self.last_result:
            messagebox.showwarning("Attention", "⚠️ No results to save. Run an analysis first.")
            return

        try:
            rows_affected = self.db_ctrl.save_ticket_responses(self.last_result)

            if rows_affected > 0:
                messagebox.showinfo("Success", f"✅ {rows_affected} records saved successfully.")
                self.clean_fields()
            else:
                messagebox.showwarning("Warning", "No changes were made to the database.")

        except Exception as e:
            messagebox.showerror("Database Error", f"Could not complete DB operation:\n\n{str(e)}")

    def refresh_output(self, text: str):
        """
        Updates the read-only output textbox with new text.
        """
        self.tb_output.configure(state="normal")
        self.tb_output.delete("1.0", "end")
        self.tb_output.insert("1.0", text)
        self.tb_output.configure(state="disabled")

    def clean_fields(self):
        """
        Resets all input fields and the results buffer to their initial state.
        """
        self._set_ui_state("normal")
        self.entry_case.delete(0, "end")

        for entry, p_key in [(self.entry1, "entry1"), (self.entry2, "entry2")]:
            entry.delete("1.0", "end")
            entry.insert("1.0", self.placeholders[p_key])
            entry.configure(text_color=self.color_placeholder)

        self.refresh_output("")
        self.last_result = []
        self.focus_set()

    def _set_ui_state(self, state: str):
        """
        Enables or disables interactive widgets during processing.
        """
        widgets = [self.entry1, self.entry2, self.entry_case, self.btn_execute, self.btn_save, self.btn_clean]
        for w in widgets:
            w.configure(state=state)