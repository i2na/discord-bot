import re
import time
import requests
import datetime
from config.constants import Constants

ARTICLE_SEPARATOR = "\n---\n"
EMBED_DESCRIPTION_LIMIT = 4096
POST_DELAY_SEC = 1.5

def _split_body(body, max_len):
    if len(body) <= max_len:
        return [body]
    chunks = []
    remaining = body
    while remaining:
        if len(remaining) <= max_len:
            chunks.append(remaining)
            break
        cut = remaining[:max_len]
        last_para = cut.rfind("\n\n")
        if last_para > max_len // 2:
            chunks.append(remaining[:last_para + 1].strip())
            remaining = remaining[last_para + 1:].strip()
        else:
            last_newline = cut.rfind("\n")
            if last_newline > max_len // 2:
                chunks.append(remaining[:last_newline + 1].strip())
                remaining = remaining[last_newline + 1:].strip()
            else:
                chunks.append(remaining[:max_len])
                remaining = remaining[max_len:].strip()
    return chunks

def _parse_articles(content):
    raw_blocks = [b.strip() for b in content.split(ARTICLE_SEPARATOR) if b.strip()]
    articles = []
    for block in raw_blocks:
        match = re.match(r'^## (\d+)\. \[(.+?)\]\((https?://[^\)]+)\)', block)
        if match:
            idx, title, url = match.group(1), match.group(2), match.group(3)
            body = block[match.end():].strip()
            articles.append({"idx": idx, "title": title, "url": url, "body": body})
    return articles

def send_to_discord(content):
    webhook_url = Constants.DISCORD_WEBHOOK_URL
    if not webhook_url:
        return "Error: Webhook URL missing"
    today = datetime.datetime.now().strftime("%Y년 %m월 %d일")
    header_msg = f"# 📰 {today} 시사 브리핑\n오늘 꼭 알아야 할 뉴스 5가지를 정리해 드립니다."
    header_data = {"content": header_msg, "username": Constants.BOT_NAME, "avatar_url": Constants.BOT_AVATAR_URL}
    resp = requests.post(webhook_url, json=header_data)
    resp.raise_for_status()
    articles = _parse_articles(content)
    if articles:
        for a in articles:
            time.sleep(POST_DELAY_SEC)
            body_chunks = _split_body(a["body"], EMBED_DESCRIPTION_LIMIT)
            for i, chunk in enumerate(body_chunks):
                if i > 0:
                    time.sleep(POST_DELAY_SEC)
                title = f"{a['idx']}. {a['title']}"
                if len(body_chunks) > 1:
                    title = f"{title} ({i+1}/{len(body_chunks)})"
                title = title[:256]
                embed = {"title": title, "url": a["url"], "description": chunk, "color": 5814783}
                data = {"embeds": [embed], "username": Constants.BOT_NAME, "avatar_url": Constants.BOT_AVATAR_URL}
                resp = requests.post(webhook_url, json=data)
                resp.raise_for_status()
        return "Report Sent Successfully"
    final_content = content
    chunk_size = Constants.DISCORD_CHUNK_SIZE
    chunks = [final_content[i:i+chunk_size] for i in range(0, len(final_content), chunk_size)]
    for chunk in chunks:
        time.sleep(POST_DELAY_SEC)
        data = {"content": chunk, "username": Constants.BOT_NAME, "avatar_url": Constants.BOT_AVATAR_URL}
        resp = requests.post(webhook_url, json=data)
        resp.raise_for_status()
    return "Report Sent Successfully"