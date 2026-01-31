import os

class Constants:
    # 1. 환경 변수
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")
    OPENAI_MODEL = "gpt-4o"
    
    # 2. 크롤링 설정
    USER_AGENT = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    # [URL, Source Name, Fetch Limit]
    NEWS_SOURCES = [
        ("https://news.naver.com/main/rss/rss_flash.nhn?mode=LSD&mid=sec&sid1=101", "Naver Economy", 5),
        ("https://www.mk.co.kr/rss/30000001/", "MK News", 5),
        ("https://fs.jtbc.co.kr/RSS/newsflash.xml", "JTBC News", 5)
    ]

    # 3. 디스코드 봇 설정
    BOT_NAME = "SISA-GO"
    BOT_AVATAR_URL = "https://cdn-icons-png.flaticon.com/512/2965/2965879.png"
    DISCORD_CHUNK_SIZE = 1900