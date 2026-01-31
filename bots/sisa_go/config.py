import os
from core import BotConfig

config = BotConfig(
    name="SISA-GO",
    sources=[
        (
            "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx1YlY4U0FtdHZHZ0pMVWlnQVAB?hl=ko&gl=KR&ceid=KR:ko",
            "World",
            5
        ),
        (
            "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx6TVdZU0FtdHZHZ0pMVWlnQVAB?hl=ko&gl=KR&ceid=KR:ko",
            "Business",
            5
        ),
        (
            "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGRqTVhZU0FtdHZHZ0pMVWlnQVAB?hl=ko&gl=KR&ceid=KR:ko",
            "Technology",
            5
        ),
    ],
    prompt_path=os.path.join(os.path.dirname(__file__), "prompt.txt"),
    webhook_url=os.environ.get("SISA_GO_WEBHOOK_URL"),
    avatar_url="https://cdn-icons-png.flaticon.com/512/2965/2965879.png",
)
