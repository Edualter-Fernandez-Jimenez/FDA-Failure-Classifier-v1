from openai import OpenAI
from typing import Optional


class LLMClient:
    def __init__(self, base_url: str = "http://192.168.0.13:8080/v1", api_key: str = "lm-studio"):
        """
        Cliente para interactuar con LM Studio u otros servicios compatibles con OpenAI API.
        """
        self.client = OpenAI(base_url=base_url, api_key=api_key)
        # Definimos el modelo por defecto como un atributo de clase
        self.default_model = "qwen2.5-7b-instruct-1m"

    def get_classification(self, sys_context: str, user_prompt: str) -> Optional[str]:
        """
        Envía una solicitud al modelo y retorna la clasificación en mayúsculas.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.default_model,
                messages=[
                    {"role": "system", "content": sys_context},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.0,
                timeout=30.0  # Evita que el programa espere infinitamente
            )

            content = response.choices[0].message.content
            return content.strip().upper() if content else None

        except Exception as e:
            raise Exception(f"ERROR EN LLM_CLIENT: {e}")