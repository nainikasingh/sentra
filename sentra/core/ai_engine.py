# # core/ai_engine.py
# import os
# import logging
# from typing import Optional
# import requests
# import ollama  # Ollama Python client

# # Configure logging
# logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
# logger = logging.getLogger(__name__)

# class AIEngine:
#     def __init__(self):
#         self.mode = self._detect_mode()
#         self.local_model = os.getenv("LOCAL_MODEL", "llama3:8b-instruct-q4")
#         self.api_endpoint = os.getenv("API_ENDPOINT", "https://api.openai.com/v1/chat/completions")
#         self.api_key = os.getenv("API_KEY")

#         # Validate critical configurations
#         if self.mode == "api" and not self.api_key:
#             raise ValueError("API_KEY is required for API mode.")
#         if not self.local_model:
#             raise ValueError("LOCAL_MODEL is not configured.")

#     def _detect_mode(self) -> str:
#         """Auto-switch based on network/requirements."""
#         if os.getenv("AIRGAPPED", "false").lower() == "true":
#             logger.info("AIRGAPPED mode detected. Using local mode.")
#             return "local"
#         try:
#             requests.get("https://google.com", timeout=3)
#             logger.info("Internet connection detected. Using API mode.")
#             return "api"
#         except requests.RequestException:
#             logger.warning("No internet connection detected. Falling back to local mode.")
#             return "local"

#     def generate(self, prompt: str, max_tokens: int = 512) -> Optional[str]:
#         """Unified LLM call with failover."""
#         try:
#             if self.mode == "api":
#                 return self._call_api(prompt, max_tokens)
#             else:
#                 return self._call_local(prompt, max_tokens)
#         except Exception as e:
#             logger.error(f"LLM Error: {e}")
#             return None

#     def _call_api(self, prompt: str, max_tokens: int) -> str:
#         """Call external LLM API (e.g., OpenAI)."""
#         headers = {"Authorization": f"Bearer {self.api_key}"}
#         data = {
#             "model": "gpt-4-turbo",
#             "messages": [{"role": "user", "content": prompt}],
#             "max_tokens": max_tokens
#         }
#         try:
#             response = requests.post(self.api_endpoint, json=data, headers=headers, timeout=10)
#             response.raise_for_status()
#             return response.json()["choices"][0]["message"]["content"]
#         except requests.RequestException as e:
#             logger.error(f"API call failed: {e}")
#             raise

#     def _call_local(self, prompt: str, max_tokens: int) -> str:
#         """Call local Ollama instance."""
#         try:
#             response = ollama.generate(
#                 model=self.local_model,
#                 prompt=prompt,
#                 options={"num_predict": max_tokens}
#             )
#             return response["response"]
#         except Exception as e:
#             logger.error(f"Local model call failed: {e}")
#             raise

# # Example usage
# if __name__ == "__main__":
#     try:
#         ai = AIEngine()
#         result = ai.generate("Summarize the latest security alerts in one line.")
#         if result:
#             logger.info(f"Generated response: {result}")
#         else:
#             logger.warning("No response generated.")
#     except Exception as e:
#         logger.critical(f"Failed to initialize AIEngine: {e}")

# interface/cli.py
# /home/xenin/sentra/sentra/core/ai_engine.py
import os
import ollama

class AIEngine:
    def __init__(self):
        self.local_model = "llama3:latest"

    def generate(self, prompt: str) -> str:
        response = ollama.generate(
            model=self.local_model,
            prompt=f"Answer as a cybersecurity expert: {prompt}"
        )
        return response["response"]

# Test directly
if __name__ == "__main__":
    ai = AIEngine()
    print(ai.generate("Is port 22 open?"))