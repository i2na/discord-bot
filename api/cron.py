from http.server import BaseHTTPRequestHandler
import os
import json
import xml.etree.ElementTree as ET
from openai import OpenAI
import requests

# 1. 환경 변수 설정
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

client = OpenAI(api_key=OPENAI_API_KEY)

# 2. 뉴스 수집 함수 (3중 안전장치)
def fetch_rss(url, source_name):
    print(f"Attempting to fetch from: {source_name}...")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8' # 한글 깨짐 방지
        
        if response.status_code != 200:
            print(f"Failed {source_name}: Status {response.status_code}")
            return None

        root = ET.fromstring(response.content)
        news_list = []
        count = 0
        
        for item in root.findall('.//item'):
            if count >= 5: break
            
            title = item.find('title').text
            link = item.find('link').text
            
            # 설명 가져오기 (없을 경우 대비)
            desc_node = item.find('description')
            description = desc_node.text if desc_node is not None else ""
            
            # HTML 태그 제거 및 정리
            if description:
                description = description.replace('<b>', '').replace('</b>', '').replace('&quot;', '"').replace('<![CDATA[', '').replace(']]>', '')
                if len(description) > 200: description = description[:200] + "..."
            
            # 날짜(선택사항)
            date_node = item.find('pubDate')
            date = date_node.text if date_node is not None else ""

            news_list.append(f"Source: {source_name}\nTitle: {title}\nLink: {link}\nDate: {date}\nSummary: {description}\n---")
            count += 1
            
        if not news_list:
            return None
            
        return "\n".join(news_list)

    except Exception as e:
        print(f"Error fetching {source_name}: {str(e)}")
        return None

def get_news_robust():
    # [1순위] 네이버 금융(경제) 속보 RSS (가장 빠르고 정확함)
    res = fetch_rss("https://news.naver.com/main/rss/rss_flash.nhn?mode=LSD&mid=sec&sid1=101", "Naver Economy")
    if res: return res

    # [2순위] 매일경제 주요뉴스 RSS (경제지 중 신뢰도 높음)
    res = fetch_rss("https://www.mk.co.kr/rss/30000001/", "MK News")
    if res: return res
    
    # [3순위] 구글 뉴스 (최후의 보루)
    res = fetch_rss("https://news.google.com/rss/search?q=한국경제+주요뉴스+when:1d&hl=ko&gl=KR&ceid=KR:ko", "Google News")
    if res: return res
    
    return None

# 3. LLM 분석 함수 (Shadow Analyst)
def analyze_news(news_text):
    if not news_text:
        return "정보 입수 실패. 모든 보안 채널이 차단되었습니다."

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

    try:
        response = client.chat.completions.create(
            model="gpt-4o", 
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Here is the intercepted intel:\n{news_text}"}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Decryption Failed (LLM Error): {str(e)}"

# 4. 디스코드 전송 함수
def send_to_discord(content):
    if not DISCORD_WEBHOOK_URL:
        return "Error: Webhook URL missing"
        
    data = {
        "content": content,
        "username": "Shadow Analyst",
        "avatar_url": "https://cdn-icons-png.flaticon.com/512/2919/2919600.png"
    }
    try:
        requests.post(DISCORD_WEBHOOK_URL, json=data)
        return "Report Sent"
    except Exception as e:
        return f"Transmission Failed: {str(e)}"

# 5. Vercel용 핸들러
class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            print("Mission Start.")
            news = get_news_robust()
            
            if news:
                report = analyze_news(news)
                status = send_to_discord(report)
                
                self.send_response(200)
                self.end_headers()
                # 성공 시 어떤 소스에서 가져왔는지 표시
                source_used = news.split('\n')[0] 
                self.wfile.write(f'Mission Complete: {status} (via {source_used})'.encode('utf-8'))
            else:
                self.send_response(200)
                self.end_headers()
                self.wfile.write('Mission Failed: All news sources unreachable.'.encode('utf-8'))
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f'System Critical Error: {str(e)}'.encode('utf-8'))
        return