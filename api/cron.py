from http.server import BaseHTTPRequestHandler
import os
import json
from datetime import datetime
from duckduckgo_search import DDGS
from openai import OpenAI
import requests

# 1. 환경 변수 설정 (Vercel에서 설정할 것임)
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

client = OpenAI(api_key=OPENAI_API_KEY)

# 2. 뉴스 검색 함수 (무료 라이브러리 사용)
def get_news():
    print("Collecting Intel...")
    results = []
    try:
        # '한국 경제' 키워드로 최근 1일치 검색
        with DDGS() as ddgs:
            ddgs_gen = ddgs.news("한국 경제 사회 이슈", region="kr-kr", timelimit="d", max_results=5)
            for r in ddgs_gen:
                results.append(f"Title: {r['title']}\nLink: {r['url']}\nSummary: {r['body']}\n---")
    except Exception as e:
        print(f"Intel collection failed: {e}")
        return None
    
    return "\n".join(results)

# 3. LLM 분석 함수 (Shadow Analyst 페르소나)
def analyze_news(news_text):
    if not news_text:
        return "정보 입수 실패. 통신 보안 상태를 점검하십시오."

    system_prompt = """
# Role
You are a **"Shadow Analyst"** (Ghost Agent).
Your client is a young professional.
Your persona is **serious, cynical, and secretive (Noir Style).**
You treat news as "Classified Intelligence".

# Constraints
1. **LANGUAGE:** OUTPUT MUST BE IN **KOREAN**.
2. **NO EMOJIS:** Use only text symbols like `[ ]`, `//`, `>>`.
3. **LINKING:** You MUST embed the source URL into the title like `[Title](URL)`.

# Output Format
## [CLASSIFIED FILE] [Title with Link](URL)

**>> BACKGROUND INTEL**
(Explain the hidden context/history in Korean. Cynical tone.)

**>> THE EVENT**
* (Fact 1)
* (Fact 2)

**>> DECRYPTION CODE**
> **"Term"**
> (Explain a hard term with a cynical analogy.)

**>> ACTIONABLE ADVICE**
(Direct advice for a 20s pro.)

---
(Repeat for Top 3 topics)

**// END OF TRANSMISSION.**
    """

    response = client.chat.completions.create(
        model="gpt-4o", # 비용 절약하려면 "gpt-3.5-turbo"로 변경 가능
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Here is the raw intel:\n{news_text}"}
        ]
    )
    return response.choices[0].message.content

# 4. 디스코드 전송 함수
def send_to_discord(content):
    data = {
        "content": content,
        "username": "Shadow Analyst",
        "avatar_url": "https://cdn-icons-png.flaticon.com/512/2919/2919600.png" # 비밀 요원 느낌 아이콘
    }
    requests.post(DISCORD_WEBHOOK_URL, json=data)

# 5. Vercel용 핸들러 (메인 실행부)
class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        print("Mission Start.")
        news = get_news()
        if news:
            report = analyze_news(news)
            send_to_discord(report)
            self.send_response(200)
            self.end_headers()
            self.wfile.write('Mission Complete'.encode('utf-8'))
        else:
            self.send_response(500)
            self.end_headers()
            self.wfile.write('Mission Failed: No News'.encode('utf-8'))
        return