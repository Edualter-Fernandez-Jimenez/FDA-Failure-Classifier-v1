# FDA Failure Classifier 🩺🤖

An AI-driven medical device classification system built with **Python**, following a strict **MVC (Model-View-Controller)** architectural pattern. This tool leverages local Large Language Models (LLMs) to map technical problem descriptions to official **FDA MDR Annex C** codes provided by a relational database.



## 🏗️ Architecture Overview

The project is designed for high maintainability and scalability by separating the data access, business logic, and user interface:

* **Model:** Manages the lifecycle of MariaDB connections (via XAMPP) and communication with the LM Studio API.
* **Controller:** Orchestrates data flow, cleans results with Pandas, and manages "Retrieval-Augmented Generation" (RAG) logic by injecting database context into AI prompts.
* **View:** Provides a modern GUI using `CustomTkinter` with asynchronous threading to prevent the UI from freezing during AI inference.

---

## 🛠️ Stack & Dependencies

### 🧠 Artificial Intelligence
* **Host Program:** [LM Studio](https://lmstudio.ai/)
* **LLM Model:** `qwen2.5-7b-instruct-1m`
* **Protocol:** OpenAI-compatible Local Server

### 🗄️ Database
* **Host Program:** [XAMPP](https://www.apachefriends.org/)
* **Engine:** MariaDB (Relational)
* **Database Name:** `fda_code_classifier`

### 💻 Programming Environment
* **Language:** Python 3.10.19
* **Core Libraries:**
  * `mysql-connector-python`: For MariaDB database connectivity.
  * `openai`: For interfacing with the local LLM server.
  * `pandas`: For high-performance data manipulation and cleaning.
  * `customtkinter`: For the modern Dark Mode user interface.
  * `json`: For parsing structured AI responses.

---

## 📂 Project Structure

```text
├── main.py                     # Application Entry Point
├── controller/
│   ├── DB_controller.py        # Logic for DB-to-DataFrame transformations
│   └── llm_model_controller.py # Logic for Prompt Engineering & AI Orchestration
├── network/
│   ├── BD/
│   │   ├── Connection/         # MariaDB Connection Manager (XAMPP)
│   │   └── sql_queries.py      # Low-level SQL & Bulk Insert operations
│   └── lm_studio_service.py    # LLM Client (OpenAI API Wrapper)
├── view/
│   ├── main_page.py            # Main Layout & Navigation Manager
│   ├── llm_window.py           # Classifier Interface (Input/Output)
│   └── query_window.py         # Advanced SQL Console & Reporting
└── requirements.txt            # Project dependencies