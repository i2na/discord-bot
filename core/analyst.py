import os
from openai import OpenAI
from .interfaces import Analyst


OPENAI_MODEL = "gpt-4.1"
OPENAI_MAX_TOKENS = 16384


class OpenAIAnalyst(Analyst):
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")

    def analyze(self, content: str, prompt_path: str) -> str:
        if not self.api_key:
            return "Error: OpenAI API Key is missing."

        if not content:
            return "뉴스 수집에 실패했습니다. (No Data)"

        system_prompt = self._load_prompt(prompt_path)
        client = OpenAI(api_key=self.api_key)

        try:
            response = client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Here is the raw news feed:\n{content}"}
                ],
                temperature=0.5,
                max_tokens=OPENAI_MAX_TOKENS
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Analysis Failed: {str(e)}"

    def _load_prompt(self, prompt_path: str) -> str:
        try:
            with open(prompt_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error loading prompt file: {e}")
            return "You are a helpful news assistant. Summarize the following news."
