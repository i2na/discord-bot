from http.server import BaseHTTPRequestHandler
import os
import json
import urllib.request
import xml.etree.ElementTree as ET
from openai import OpenAI
import requests

# 1. 환경 변수 설정
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

client = OpenAI(api_key=OPENAI_API_KEY)

# 2. 뉴스 검색 함수 (구글 뉴스 RSS - 차단 없음)
def get_news():
    print("Collecting Intel from RSS...")
    # '한국 경제 사회' 키워드로 최근 24시간(when:1d) 뉴스 검색
    rss_url = "https://news.google.com/rss/search?q=한국+경제+사회+주요뉴스+when:1d&hl=ko&gl=KR&ceid=KR:ko"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    try:
        req = urllib.request.Request(rss_url, headers=headers)
        with urllib.request.urlopen(req) as response:
            xml_data = response.read()
            
        root = ET.fromstring(xml_data)
        news_list = []
        count = 0
        
        for item in root.findall('.//item'):
            if count >= 5: break # 상위 5개만
            
            title = item.find('title').text
            link = item.find('link').text
            # 설명이 없는 경우가 있어 예외처리
            desc = item.find('description')
            description = desc.text if desc is not None else "내용 요약 없음"
            
            # HTML 태그 제거 (간단하게)
            description = description.replace('<b>', '').replace('</b>', '').replace('&quot;', '"')
            
            news_list.append(f"Title: {title}\nLink: {link}\nSummary: {description}\n---")
            count += 1
            
        return "\n".join(news_list)

    except Exception as e:
        print(f"Intel collection failed: {e}")
        return None

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
**// DESTROY THIS MESSAGE AFTER READING.**
    """

    response = client.chat.completions.create(
        model="gpt-4o", 
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
        "avatar_url": "https://cdn-icons-png.flaticon.com/512/2919/2919600.png"
    }
    requests.post(DISCORD_WEBHOOK_URL, json=data)

# 5. Vercel용 핸들러
class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        print("Mission Start.")
        news = get_news()
        
        # 뉴스 데이터가 있으면 분석 시작
        if news and len(news) > 10:
            report = analyze_news(news)
            send_to_discord(report)
            self.send_response(200)
            self.end_headers()
            self.wfile.write('Mission Complete: Report Sent'.encode('utf-8'))
        else:
            self.send_response(200) # 에러로 처리하면 재시도하므로 200으로 처리하되 메시지 남김
            self.end_headers()
            self.wfile.write('Mission Incomplete: News Source Unreachable'.encode('utf-8'))
        return