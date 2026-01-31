import re
import time
import datetime
import requests
from .interfaces import Notifier, BotConfig


ARTICLE_SEPARATOR = "\n---\n"
DISCORD_CHUNK_SIZE = 1900
DISCORD_EMBED_DESCRIPTION_LIMIT = 4096
DISCORD_EMBED_TOTAL_PER_MESSAGE = 6000
DISCORD_POST_DELAY_SEC = 2


def _split_body(body: str, max_len: int) -> list:
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


def _parse_articles(content: str) -> list:
    raw_blocks = [b.strip() for b in content.split(ARTICLE_SEPARATOR) if b.strip()]
    articles = []

    for block in raw_blocks:
        match = re.match(r'^## \[(\w+)\] (\d+)\. \[(.+?)\]\((https?://[^\)]+)\)', block)
        if match:
            articles.append({
                "topic": match.group(1),
                "idx": match.group(2),
                "title": match.group(3),
                "url": match.group(4),
                "body": block[match.end():].strip()
            })

    return articles


class DiscordNotifier(Notifier):
    def _send_to_webhook(self, webhook_url: str, content: str, config: BotConfig) -> None:
        today = datetime.datetime.now().strftime("%Y년 %m월 %d일")
        header_data = {
            "content": f"# 📰 {today} 브리핑",
            "username": config.name,
            "avatar_url": config.avatar_url
        }

        resp = requests.post(webhook_url, json=header_data)
        resp.raise_for_status()

        articles = _parse_articles(content)

        if articles:
            for a in articles:
                time.sleep(DISCORD_POST_DELAY_SEC)
                body_chunks = _split_body(a["body"], DISCORD_EMBED_DESCRIPTION_LIMIT)
                batch, batch_len = [], 0

                for i, chunk in enumerate(body_chunks):
                    if batch_len + len(chunk) > DISCORD_EMBED_TOTAL_PER_MESSAGE and batch:
                        data = {"embeds": batch, "username": config.name, "avatar_url": config.avatar_url}
                        resp = requests.post(webhook_url, json=data)
                        resp.raise_for_status()
                        time.sleep(DISCORD_POST_DELAY_SEC)
                        batch, batch_len = [], 0

                    title = f"[{a['topic']}] {a['idx']}. {a['title']}"[:256]
                    if len(body_chunks) > 1:
                        title = f"{title} ({i+1}/{len(body_chunks)})"[:256]

                    batch.append({"title": title, "url": a["url"], "description": chunk, "color": 5814783})
                    batch_len += len(chunk)

                if batch:
                    data = {"embeds": batch, "username": config.name, "avatar_url": config.avatar_url}
                    resp = requests.post(webhook_url, json=data)
                    resp.raise_for_status()
            return

        chunks = [content[i:i+DISCORD_CHUNK_SIZE] for i in range(0, len(content), DISCORD_CHUNK_SIZE)]
        for chunk in chunks:
            time.sleep(DISCORD_POST_DELAY_SEC)
            data = {"content": chunk, "username": config.name, "avatar_url": config.avatar_url}
            resp = requests.post(webhook_url, json=data)
            resp.raise_for_status()

    def notify(self, content: str, config: BotConfig) -> str:
        if not config.webhook_url:
            return "Error: Webhook URL missing"

        webhook_urls = [url.strip() for url in config.webhook_url.split(",") if url.strip()]

        for i, url in enumerate(webhook_urls):
            print(f"[{config.name}] Sending to webhook {i+1}/{len(webhook_urls)}")
            self._send_to_webhook(url, content, config)

        return f"Report Sent Successfully to {len(webhook_urls)} webhook(s)"
