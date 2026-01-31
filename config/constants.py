import os

class Constants:
    # 1. 환경 변수
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")
    OPENAI_MODEL = "gpt-4.1"
    OPENAI_MAX_TOKENS = 16384
    
    # 2. 크롤링 설정
    USER_AGENT = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    # [URL, Source Name, Fetch Limit]
    # Google News RSS (Korea): World, Business, Technology - 중요도 기준 정렬
    NEWS_SOURCES = [
        ("https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx1YlY4U0FtdHZHZ0pMVWlnQVAB?hl=ko&gl=KR&ceid=KR:ko", "World", 5),
        ("https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx6TVdZU0FtdHZHZ0pMVWlnQVAB?hl=ko&gl=KR&ceid=KR:ko", "Business", 5),
        ("https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGRqTVhZU0FtdHZHZ0pMVWlnQVAB?hl=ko&gl=KR&ceid=KR:ko", "Technology", 5),
    ]

    # 3. 디스코드 봇 설정
    BOT_NAME = "SISA-GO"
    BOT_AVATAR_URL = "https://cdn-icons-png.flaticon.com/512/2965/2965879.png"
    DISCORD_CHUNK_SIZE = 1900
    DISCORD_EMBED_DESCRIPTION_LIMIT = 4096
    DISCORD_EMBED_TOTAL_PER_MESSAGE = 6000
    DISCORD_POST_DELAY_SEC = 2