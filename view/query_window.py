"""
SQL Console View Module for the FDA Classifier.

This module implements an advanced SQL interface using CustomTkinter,
enabling raw query execution, dynamic data rendering in a scrollable grid,
and multi-format report exportation.
"""

import customtkinter as ctk
import pandas as pd
import threading
from tkinter import messagebox, filedialog, Canvas
from typing import Optional


class QueryWindow(ctk.CTkFrame):
    """
    Advanced SQL console frame for database querying and reporting.

    Attributes:
        db_ctrl (DBController): Controller responsible for executing custom SQL.
        last_df (Optional[pd.DataFrame]): Stores the result of the last successful query.
    """

    def __init__(self, master, db_controller, **kwargs):
        """
        Initializes the SQL console with connection settings and UI defaults.

        Args:
            master: The parent widget.
            db_controller (DBController): Orchestrator for custom database queries.
        """
        super().__init__(master, **kwargs)

        self.db_ctrl = db_controller
        self.last_df: Optional[pd.DataFrame] = None

        # Initial text configuration
        self.placeholder_sql = "-- Type your SQL query here...\nSELECT * FROM event_ticket_response LIMIT 50;"

        # Consistent colors
        self.color_placeholder = "gray"
        self.color_normal = ("black", "white")  # (Light mode, Dark mode)

        self._setup_ui()

    def _setup_ui(self):
        """
        Configures the widget hierarchy and layout for the console.
        """
        self.lb_title = ctk.CTkLabel(
            self,
            text="SQL ADVANCED CONSOLE",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        self.lb_title.pack(pady=(20, 10))

        self.input_container = ctk.CTkFrame(self, fg_color="transparent")
        self.input_container.pack(fill="x", padx=20)

        self.lb_instruction = ctk.CTkLabel(self.input_container, text="SQL Query:", anchor="w",
                                           font=("Roboto", 12, "bold"))
        self.lb_instruction.pack(fill="x", pady=(5, 2))

        # Textbox for the full query
        self.txt_sql = ctk.CTkTextbox(
            self.input_container,
            height=180,
            border_width=1,
            font=("Consolas", 13),
            text_color=self.color_placeholder
        )
        self.txt_sql.pack(fill="x", pady=(0, 10))
        self.txt_sql.insert("1.0", self.placeholder_sql)

        # Placeholder management events
        self.txt_sql.bind("<FocusIn>", lambda e: self._handle_placeholder("in"))
        self.txt_sql.bind("<FocusOut>", lambda e: self._handle_placeholder("out"))

        self.lb_table = ctk.CTkLabel(self, text="Data Preview:", anchor="w", font=("Roboto", 12, "bold"))
        self.lb_table.pack(fill="x", padx=20, pady=(10, 0))

        self._setup_table_area()
        self._create_buttons()

    def _setup_table_area(self):
        """
        Prepares the scrollable canvas and interior frame for data rendering.
        """
        self.table_main_container = ctk.CTkFrame(self)
        self.table_main_container.pack(fill="both", expand=True, padx=20, pady=5)

        self.canvas = Canvas(
            self.table_main_container,
            bg=self._apply_appearance_mode(self._fg_color),
            highlightthickness=0,
            bd=0
        )
        self.canvas.grid(row=0, column=0, sticky="nsew")

        self.v_scroll = ctk.CTkScrollbar(self.table_main_container, orientation="vertical", command=self.canvas.yview)
        self.v_scroll.grid(row=0, column=1, sticky="ns")

        self.h_scroll = ctk.CTkScrollbar(self.table_main_container, orientation="horizontal", command=self.canvas.xview)
        self.h_scroll.grid(row=1, column=0, sticky="ew")

        self.canvas.configure(yscrollcommand=self.v_scroll.set, xscrollcommand=self.h_scroll.set)

        self.table_interior_frame = ctk.CTkFrame(self.canvas, fg_color="transparent")
        self.canvas.create_window((0, 0), window=self.table_interior_frame, anchor="nw")

        self.table_main_container.grid_rowconfigure(0, weight=1)
        self.table_main_container.grid_columnconfigure(0, weight=1)

        self.table_interior_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

    def _handle_placeholder(self, mode: str):
        """
        Manages focus-based placeholder text for the SQL input.

        Args:
            mode (str): "in" for gaining focus, "out" for losing focus.
        """
        current_text = self.txt_sql.get("1.0", "end-1c").strip()

        if mode == "in":
            if current_text == self.placeholder_sql.strip():
                self.txt_sql.delete("1.0", "end")
                self.txt_sql.configure(text_color=self.color_normal)

        elif mode == "out":
            if not current_text:
                self.txt_sql.insert("1.0", self.placeholder_sql)
                self.txt_sql.configure(text_color=self.color_placeholder)

    def _create_buttons(self):
        """
        Builds the control buttons for query execution and reporting.
        """
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(fill="x", padx=20, pady=(10, 20))

        ctk.CTkButton(
            self.button_frame,
            text="Clear Console",
            fg_color="#4a4a4a",
            hover_color="#333333",
            width=120,
            command=self.clean_fields
        ).pack(side="left")

        self.btn_execute = ctk.CTkButton(
            self.button_frame,
            text="Run Query",
            fg_color="#2ecc71",
            hover_color="#27ae60",
            font=ctk.CTkFont(weight="bold"),
            command=self.execute_query
        )
        self.btn_execute.pack(side="right", padx=(10, 0))

        self.btn_report = ctk.CTkButton(
            self.button_frame,
            text="Export to File",
            command=self.generate_report
        )
        self.btn_report.pack(side="right", padx=10)

    def execute_query(self):
        """
        Validates the SQL input and starts the execution thread.
        """
        query_text = self.txt_sql.get("1.0", "end-1c").strip()

        if not query_text or query_text == self.placeholder_sql.strip():
            messagebox.showwarning("Input Empty", "Please enter a valid SQL query.")
            return

        self._set_ui_state("disabled")
        threading.Thread(target=self._query_thread, args=(query_text,), daemon=True).start()

    def _query_thread(self, query: str):
        """
        Executes the query in a background thread and manages the state of the table.

        Args:
            query (str): The raw SQL statement to execute.
        """
        try:
            df_result = self.db_ctrl.get_custom_query(query)
            self.last_df = df_result
            self.after(0, lambda: self.load_dynamic_table(df_result))

        except ValueError as ve:
            msg = str(ve)
            self.after(0, lambda: messagebox.showwarning("No Data", f"⚠️ {msg}"))
            self.after(0, lambda: self.load_dynamic_table(pd.DataFrame()))

        except Exception as e:
            error_msg = str(e)
            self.after(0, lambda: messagebox.showerror("Database Error", f"Execution failed:\n\n{error_msg}"))
            self.after(0, lambda: self.load_dynamic_table(pd.DataFrame()))

        finally:
            self.after(0, lambda: self._set_ui_state("normal"))

    def load_dynamic_table(self, df: pd.DataFrame):
        """
        Renders a Pandas DataFrame into the scrollable UI grid.

        Args:
            df (pd.DataFrame): The data to be displayed in the console.
        """
        for widget in self.table_interior_frame.winfo_children():
            widget.destroy()

        if df is None or df.empty:
            ctk.CTkLabel(self.table_interior_frame, text="No results found.").pack(pady=20)
            return

        # Render Headers
        for col, col_name in enumerate(df.columns):
            ctk.CTkLabel(
                self.table_interior_frame,
                text=str(col_name).upper(),
                font=("Roboto", 11, "bold"),
                fg_color="#333333",
                text_color="white",
                width=150,
                height=30
            ).grid(row=0, column=col, padx=1, pady=1, sticky="nsew")

        # Render Rows (Limit to 100 for performance)
        for row_idx, row in enumerate(df.head(100).values, start=1):
            for col_idx, value in enumerate(row):
                ctk.CTkLabel(
                    self.table_interior_frame,
                    text=str(value),
                    fg_color="#2b2b2b",
                    width=150,
                    height=25
                ).grid(row=row_idx, column=col_idx, padx=1, pady=1, sticky="nsew")

    def generate_report(self):
        """
        Saves the result of the last successful query to a CSV or Excel file.
        """
        if self.last_df is None or self.last_df.empty:
            messagebox.showwarning("Warning", "There is no data loaded to export.")
            return

        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV File", "*.csv"), ("Excel File", "*.xlsx")]
        )

        if path:
            try:
                if path.endswith('.xlsx'):
                    self.last_df.to_excel(path, index=False)
                else:
                    self.last_df.to_csv(path, sep=",", index=False, encoding="utf-8-sig")
                messagebox.showinfo("Success", "Report saved successfully.")
            except Exception as e:
                messagebox.showerror("Export Error", f"Could not save file:\n{e}")

    def clean_fields(self):
        """
        Resets the console input, results table, and temporary memory.
        """
        for widget in self.table_interior_frame.winfo_children():
            widget.destroy()
        self.last_df = None

        self.txt_sql.delete("1.0", "end")
        self.txt_sql.insert("1.0", self.placeholder_sql)
        self.txt_sql.configure(text_color=self.color_placeholder)
        self.focus_set()

    def _set_ui_state(self, state: str):
        """
        Toggles the interactive state of the control buttons.
        """
        s = "normal" if state == "normal" else "disabled"
        self.btn_execute.configure(state=s)
        self.btn_report.configure(state=s)