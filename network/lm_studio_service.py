"""
LLM Client Module for the FDA Classifier.

This module manages the interface between the application and Large Language Models
(LLMs), specifically optimized for local inference engines like LM Studio.
"""

from openai import OpenAI
from typing import Optional


class LLMClient:
    """
    Client for interacting with LM Studio or OpenAI-compatible API services.

    Attributes:
        client (OpenAI): The initialized OpenAI client instance.
        default_model (str): The identifier of the model used for classification.
    """

    def __init__(self, base_url: str = "http://192.168.0.13:8080/v1", api_key: str = "lm-studio"):
        """
        Initializes the LLMClient with server credentials and connection parameters.

        Args:
            base_url (str): The endpoint URL for the API. Defaults to local LM Studio instance.
            api_key (str): The authorization key. Defaults to "lm-studio".
        """
        self.client = OpenAI(base_url=base_url, api_key=api_key)
        # Defining the default model as a class attribute
        self.default_model = "qwen2.5-7b-instruct-1m"

    def get_classification(self, sys_context: str, user_prompt: str) -> Optional[str]:
        """
        Sends a request to the model and returns the classification in uppercase.

        This method uses a temperature of 0.0 to ensure deterministic results,
        which is critical for consistent classification logic.

        Args:
            sys_context (str): The system prompt defining the model's persona and rules.
            user_prompt (str): The specific input data or text to be classified.

        Returns:
            Optional[str]: The model's response processed in uppercase, or None if empty.

        Raises:
            Exception: If the API request fails or the connection times out.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.default_model,
                messages=[
                    {"role": "system", "content": sys_context},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.0,
                timeout=30.0  # Prevents the program from waiting indefinitely
            )

            content = response.choices[0].message.content
            return content.strip().upper() if content else None

        except Exception as e:
            raise Exception(f"ERROR IN LLM_CLIENT: {e}")