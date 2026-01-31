import os
from openai import OpenAI
from config.constants import Constants

def load_prompt():
    try:
        current_dir = os.path.dirname(__file__)
        prompt_path = os.path.join(current_dir, '..', 'config', 'prompt.txt')
        
        with open(prompt_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error loading prompt file: {e}")
        return "You are a helpful news assistant. Summarize the following news."

def analyze_news(news_text):
    if not Constants.OPENAI_API_KEY:
        return "Error: OpenAI API Key is missing."
        
    client = OpenAI(api_key=Constants.OPENAI_API_KEY)

    if not news_text:
        return "뉴스 수집에 실패했습니다. (No Data)"

    system_prompt = load_prompt()

    try:
        response = client.chat.completions.create(
            model=Constants.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Here is the raw news feed:\n{news_text}"}
            ],
            temperature=0.5,
            max_tokens=Constants.OPENAI_MAX_TOKENS
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Analysis Failed: {str(e)}"